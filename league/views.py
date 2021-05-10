from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import F
from auction.models import Original_Team, Player, Stats, Team
from .cricapi import league_teams, get_scorecard, get_matches
from league.tasks import update_player_stats, get_league_teams

# Create your views here.


def player_stats(request):
    if request.method == 'POST' and 'update_points' in request.POST:
        get_league_teams.delay()
        update_player_stats.delay()
        messages.success(
            request, f'Queued Player status update successfully')
    stats = Stats.objects.all().annotate(ordering=2*F('runs')+25 *
                                         F('wickets')).order_by('-ordering')
    return render(request, 'league/stats.html', {'stats': stats})


def team_standings(request):
    return redirect('index')
