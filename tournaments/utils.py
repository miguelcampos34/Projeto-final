from .models import Match



def calculate_elo(white_rating, black_rating, result, k_factor=32):
    expected_white = 1/(1 + 10**((black_rating - white_rating) / 400))
    expected_black = 1/(1 + 10**((white_rating - black_rating) / 400))

    if result == "1-0":
        score_white, score_black = 1.0, 0.0

    elif result == "0-1":
        score_white, score_black = 0.0, 1.0

    else:
        score_white, score_black = 0.5, 0.5

    new_white_rating = round(white_rating + k_factor * (score_white - expected_white))
    new_black_rating = round(black_rating + k_factor * (score_black - expected_black))

    return new_white_rating, new_black_rating

def generate_round_pairings(tournament):
    players = list(tournament.players.all().order_by("-points", "-rating"))

    past_matches = tournament.matches.all()
    played_pairs = {
        frozenset([m.white_player.id, m.black_player.id])
        for m in past_matches
    }

    unpaired = players.copy()
    pairings = []

    while len(unpaired) >= 2:
        p1 = unpaired.pop(0)
        opponent_index = None

        for i, candidate in enumerate(unpaired):
            if frozenset([p1.id, candidate.id]) not in played_pairs:
                opponent_index = i
                break

        if opponent_index is None:
            opponent_index = 0

        p2 = unpaired.pop(opponent_index)

        p1_whites = Match.objects.filter(tournament=tournament, white_player=p1).count()
        p2_whites = Match.objects.filter(tournament=tournament, white_player=p2).count()

        if p1_whites <= p2_whites:
            white, black = p1, p2
        else:
            white, black = p2, p1

        pairings.append((white, black))


    if len(unpaired) == 1:
        bye_player = unpaired[0]
        bye_player.points += 1.0
        bye_player.save()

    for white, black in pairings:
        Match.objects.create(
            tournament=tournament,
            round_number=tournament.current_round,
            white_player=white,
            black_player=black
        )