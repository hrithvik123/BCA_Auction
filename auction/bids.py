from .models import Auction, Bid
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

# function that palces a bid


def placeBid(bid, auction):
    """
    Removes €1.0 from user.
    Creates a Bid record
    Increases the auction's number of bids

    Parameters
    ----------
    auction : class 'website.models.Auction
    """
    """
    """
    ###
    if(auction.winning_price < bid.amount):
        auction.winning_bid = bid.amount
        auction.winning_user = bid.user_id
        auction.number_of_bids += 1
        auction.save()

    ###


def remaining_time(auction):
    """
    Calculates the auction's remaining time
    in minutes and seconds and converts them 
    into a string.

    Parameters
    ----------
    auction : class 'website.models.Auction

    Returns
    -------

    time_left : str
        string representation of remaining time in
        minutes and seconds.
    expired : int
        if the value is less than zero then the auction ended.

    """
    time_left = auction.time_ending - timezone.now()
    days, seconds = time_left.days, time_left.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    time_left = str(minutes) + "m " + str(seconds) + "s"
    expired = days

    return time_left, expired