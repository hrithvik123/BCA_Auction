from django.urls import path, include
from . import views as league_views
from allauth.account.views import LoginView, LogoutView, PasswordResetView

urlpatterns = [
    path('fetch_teams/', league_views.get_league_teams, name='fetch-teams'),
    path('update_stats/', league_views.update_stats, name='update-stats')
]
