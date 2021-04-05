from django.urls import path, include
from . import views as auction_views
from allauth.account.views import LoginView, LogoutView, PasswordResetView

urlpatterns = [
    path('', auction_views.home, name='index'),
    path('register/', auction_views.register, name='register'),
    path('login/', LoginView.as_view(template_name='auction/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='auction/logout.html'), name='logout'),
    path('password_reset/', PasswordResetView.as_view(
         template_name='auction/password_reset.html'), name='reset_password'),
    path('team/<str:pk>/', auction_views.updateTeamView.as_view(), name='team-edit'),
    path('team/list',
         auction_views.TeamLineUpListView.as_view(), name='lineup'),
    path('auctions/list', auction_views.AuctionListView.as_view(),
         name='auction-list'),
    path('auctions/new', auction_views.AuctionCreateView.as_view(),
         name='auction-new'),
    path('players/list', auction_views.PlayerListView.as_view(),
         name='player-list'),
    path('players/new', auction_views.PlayerCreateView.as_view(),
         name='player-new'),
    path('bids/new', auction_views.BidCreateView.as_view(), name='bid-new'),
    path('bids/list', auction_views.BidListView.as_view(), name='bid-list')
]
