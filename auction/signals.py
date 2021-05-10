from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Team, Player, Bidder, Auction, Bid, Stats
from django.utils import timezone


# make a bid
@receiver(post_save, sender=Bid)
def create_bid(sender, instance, created, **kwargs):
    if created:
        if instance.bid_time <= instance.auction_id.end_time:
            amount = instance.amount
            if(amount > instance.auction_id.winning_price):
                # update previous highest bidder's amount
                if(instance.auction_id.winning_team != None):
                    instance.auction_id.winning_team.balance += instance.auction_id.winning_price
                    instance.auction_id.winning_team.save()
                instance.auction_id.winning_price = amount
                instance.auction_id.winning_team = instance.team
                instance.auction_id.save()
                instance.team.balance -= amount
                instance.team.save()


# change auction status
@receiver(post_save, sender=Auction)
def save_auction(sender, instance, created, **kwargs):
    if not created:
        instance.player_id.team = instance.winning_team
        instance.player_id.save()


@receiver(post_save, sender=Player)
def create_stats(sender, instance, created, **kwargs):
    if created:
        stats_row = Stats()
        stats_row.player = instance
        stats_row.runs = 0
        stats_row.wickets = 0
        stats_row.save()


@receiver(post_save, sender=User)
def create_team(sender, instance, created, **kwargs):
    if created:
        new_team = Team()
        new_team.owner_id = instance
        new_team.save()
