from django.conf import settings
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignupForm

# FBV Example
# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             return redirect(settings.LOGIN_URL)
#     else:
#         form = UserCreationForm()
#     return render(request, 'accounts/signup.html', {'form': form, })

signup = CreateView.as_view(
            template_name='accounts/signup.html',
            model=User,
            form_class=SignupForm,
            success_url=settings.LOGIN_URL)

@login_required # settings.LOGIN_URL
def profile(request):
    return render(request, 'accounts/profile.html')
