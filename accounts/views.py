from django.conf import settings
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, resolve_url
from .forms import SignupForm

# FBV Example
# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             #  로그인 처리
#             auth_login(request, user)
#             next_url = request.GET.get('next') or 'profile'
#             return redirect(next_url)
#     else:
#         form = UserCreationForm()
#     return render(request, 'accounts/signup.html', {'form': form, })

class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'accounts/signup.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next') or 'profile'
        return resolve_url(next_url)

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return redirect(self.get_success_url())

signup = SignupView.as_view()


@login_required # settings.LOGIN_URL
def profile(request):
    return render(request, 'accounts/profile.html')
