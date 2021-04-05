from django.contrib import admin
from .models import Bid, Team, Auction, Player, Bidder, Chat
# Register your models here.
admin.site.register(Bid)
admin.site.register(Team)
admin.site.register(Auction)
admin.site.register(Player)
admin.site.register(Bidder)
admin.site.register(Chat)
