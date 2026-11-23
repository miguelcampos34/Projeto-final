from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .utils import calculate_elo
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseForbidden, request
from .models import Tournament 
from django.urls import reverse
from .models import User, Player
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
    query = request.GET.get("q", "").strip()
    tournaments = Tournament.objects.all()

    if query:
        tournaments = tournaments.filter(name__icontains=query)

    tournaments = tournaments.order_by("-date")

    return render(request, "tournaments/index.html", {
        "tournaments": tournaments,
        "query": query
    })

def login_view(request):
    if request.method == "POST":
    
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
    
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "tournaments/login.html", {
                "message": "Nome de usuário e/ou senha inválidos."
                })
    else:
        return render(request, "tournaments/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "tournaments/register.html", {
                "message": "As senhas devem coincidir."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "tournaments/register.html", {
                "message": "Nome de usuário já está em uso."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "tournaments/register.html")


@login_required
def create_tournament(request):
    if request.method != "POST":
        return render(request, "tournaments/create_tournament.html")

    name = request.POST.get("name", "").strip()
    rounds_raw = request.POST.get("rounds", "5").strip()

    if name:
        rounds = int(rounds_raw) if rounds_raw.isdigit() else 5
        if not 1<= rounds <= 15:
            rounds = 5

        tournament = Tournament.objects.create(
            name=name,
            rounds = rounds,
            organizer = request.user
        )
        return HttpResponseRedirect(reverse("tournament_detail", args=(tournament.id,)))
    
    return render(request, "tournaments/create_tournament.html")

def tournament_detail(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    players = tournament.players.all().order_by("name")
    standings = tournament.players.all().order_by("-points", "-rating")
    matches = tournament.matches.filter(round_number=tournament.current_round)

    return render(request, "tournaments/tournament_detail.html", {
        "tournament": tournament,
        "players": players,
        "standings": standings,
        "matches": matches
    })


@login_required
def add_player(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)

    if request.user != tournament.organizer:
        return HttpResponseForbidden("Acesso negado")

    if tournament.status != Tournament.Choice.REGISTRATION:
        return HttpResponseRedirect(reverse("tournament_detail", args=(tournament.id,)))

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        rating_raw = request.POST.get("rating", "1200").strip()

        if name:
            rating = int(rating_raw) if rating_raw.isdigit() else 1200
            Player.objects.create(
                tournament=tournament,
                name=name,
                rating=rating
            )

    return HttpResponseRedirect(reverse("tournament_detail", args=(tournament.id,)))


def calculate_rating(request, calculate_elo):
    pass 

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        messages.success(request, f"Obrigado, {name}! Sua mensagem foi enviada com sucesso.")
    return HttpResponseRedirect(reverse("index") + "#contato")