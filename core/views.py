from django.shortcuts import render
from allauth.account.views import LoginView

class MyLoginView(LoginView):
    def get_success_url(self):
        return 'https://goldenvitpharma.com/'
