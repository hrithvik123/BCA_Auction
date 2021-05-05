from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,  # import classbased views
    CreateView,
    UpdateView,
    DeleteView
)
from .forms import UserRegistrationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from . import models
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, 'auction/index.html')


def register(request):
    if (request.method == "POST"):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save(request)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Sign up successful for {username}')
            return redirect('login')
    else:
        form = UserRegistrationForm(request.GET)
    return render(request, 'auction/register.html', {'form': form})


class updateTeamView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Team
    template_name = 'auction/team.html'
    success_url = ""
    fields = ['name']

    def form_valid(self, form):
        form.instance.owner_id = self.request.user
        return super().form_valid(form)

    def test_func(self):
        team = self.get_object()
        if(self.request.user == team.owner_id):
            return True
        return False

    def get_success_url(self):
        return reverse('lineup')

# edge case to implement - if user does not have a team, create. else go to list view


class TeamLineUpListView(LoginRequiredMixin, ListView):
    model = models.Player
    template_name = 'auction/lineup.html'
    context_object_name = 'players'

    def get_queryset(self):
        user = self.request.user
        models.Team.objects.get_or_create(owner_id=user)
        return models.Player.objects.filter(team=user.team)


class AuctionListView(LoginRequiredMixin, ListView):
    model = models.Auction
    template_name = 'auction/auction_list.html'
    context_object_name = 'auctions'

    def get_queryset(self):
        return models.Auction.objects.all()


class AuctionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = models.Auction
    fields = ['player_id', 'start_bid']
    context_object_name = 'auctions'

    def form_valid(self, form):
        form.instance.number_of_bids = 0
        return super().form_valid(form)

    def test_func(self):
        if(self.request.user.is_superuser):
            return True
        return False

    def get_success_url(self):
        return reverse('auction-list')


# class AuctionDetailView(LoginRequiredMixin, DetailView):
#     models = models.Auction


class PlayerCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = models.Player
    fields = ['name', 'original_team']
    success_url = '/players/list'
    context_object_name = 'players'

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        if(self.request.user.is_superuser):
            return True
        return False


class PlayerListView(LoginRequiredMixin, ListView):
    model = models.Player
    template_name = 'auction/players_all.html'
    context_object_name = 'players'

    def get_queryset(self):
        return models.Player.objects.all()


class BidCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = models.Bid
    fields = ['auction_id', 'amount']
    success_url = '/'

    def form_valid(self, form):
        form.instance.team_id = self.request.user.team.id
        if(form.instance.amount <= self.request.user.team.balance):
            if (form.instance.amount > form.instance.auction_id.winning_price and
                    form.instance.amount > form.instance.auction_id.start_bid):
                messages.success(self.request, f'Bid placed')
                return super().form_valid(form)
            else:
                messages.warning(
                    self.request, f'Amount bid should be greater than current bid')
                return HttpResponseRedirect(reverse('bid-new'))
        else:
            messages.warning(
                self.request, f'You cannot bid more than your balance.')
            return HttpResponseRedirect(reverse('bid-new'))

    def get_form(self, *args, **kwargs):
        form = super(BidCreateView, self).get_form(*args, **kwargs)
        form.fields['auction_id'].queryset = models.Auction.objects.filter(
            end_time__gte=timezone.now())
        return form

    def test_func(self):
        models.Team.objects.get_or_create(owner_id=self.request.user)
        return True


class BidListView(LoginRequiredMixin, ListView):
    model = models.Bid
    template_name = 'auction/bids_all.html'
    context_object_name = 'bids'

    def get_queryset(self):
        return models.Bid.objects.all()
