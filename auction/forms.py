from django import forms
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm, ResetPasswordForm
from .models import Team, Bidder, Player, Auction, Bid, Chat
from django.utils import timezone


class UserRegistrationForm(SignupForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class updateTeam(forms.ModelForm):
    name = forms.CharField(max_length=255)

    class Meta:
        model = Team
        fields = ['name']


# class createBid(forms.ModelForm):
#     class Meta:
#         model = Bid
#         fields = ['auction_id', 'amount']

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user')
#         super(createBid, self).__init__(*args, **kwargs)
#         self.fields['auction_id'].queryset = Auction.objects.get_queryset(
#             end_time <= timezone.now())
