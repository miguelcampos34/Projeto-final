from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Tournament(models.Model):
    class Choice(models.TextChoices):
        REGISTRATION = "Registration"
        IN_PROGRESS = "In Progress"
        FINISHED = "Finished"
    
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    rounds = models.IntegerField(default=5)
    current_round = models.IntegerField(default=1)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tournaments")
    status = models.CharField(choices=Choice.choices, default= Choice.REGISTRATION, max_length=20)
    
    def __str__(self):
        return f"{self.name} ({self.status})"

class Player(models.Model):
    tournament = models.ForeignKey(Tournament, related_name="players", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    rating = models.IntegerField(default= 1200)
    points = models.FloatField(default= 0.0)

    def __str__(self):
        return f"{self.name} - {self.points} pts ({self.tournament.name})"

class Match(models.Model):    
    class Result(models.TextChoices):
        PENDING = "PENDING"
        WINNER_1 = "1-0"
        WINNER_2 = "0-1"
        DRAW = "0.5-0.5"

    tournament = models.ForeignKey(Tournament, related_name="matches", on_delete=models.CASCADE)
    round_number = models.IntegerField()
    white_player = models.ForeignKey(Player, related_name="white_matches", on_delete=models.CASCADE)
    black_player = models.ForeignKey(Player, related_name="black_matches", on_delete=models.CASCADE)
    result = models.CharField(choices=Result.choices, default=Result.PENDING, max_length=20)

    def __str__(self):
        return f"{self.white_player} vs {self.black_player} ({self.result})"