from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Team, Player, Bidder, Auction, Bid, Chat
from django.utils import timezone


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


# edit
@receiver(post_save, sender=Auction)
def save_auction(sender, instance, created, **kwargs):
    if not created:
        instance.player_id.team = instance.winning_team
        instance.player_id.save()
