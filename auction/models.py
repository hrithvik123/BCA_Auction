from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta


# Create your models here.
class Team(models.Model):
    owner_id = models.OneToOneField(
        User, on_delete=models.CASCADE, unique=True)
    name = models.CharField(
        max_length=255, blank=False, default="Team")
    balance = models.DecimalField(
        max_digits=4, decimal_places=1, default=100.0)

    def __str__(self):
        return self.name


class Bidder(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.team


class Player(models.Model):
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, default=None)
    original_team = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Auction(models.Model):
    player_id = models.OneToOneField(Player, on_delete=models.CASCADE)
    number_of_bids = models.IntegerField(default=0)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(
        default=(datetime.now()+timedelta(minutes=5)))
    start_bid = models.IntegerField(default=5, blank=False)
    winning_price = models.IntegerField(default=0, blank=False)
    winning_team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, default=None)

    def __str__(self):
        return self.player_id.first_name+" "+self.player_id.last_name


class Bid(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=3, decimal_places=1)
    bid_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.auction_id


class Chat(models.Model):
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    time_send = models.DateTimeField(default=timezone.now)
