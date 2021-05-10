from django.urls import path, include
from . import views as league_views
from allauth.account.views import LoginView, LogoutView, PasswordResetView

urlpatterns = [
    # path('fetch_teams/', league_views.get_league_teams, name='fetch-teams'),
    path('players/all', league_views.player_stats, name='player-list'),
    path('standings/', league_views.team_standings, name='standings')
]
