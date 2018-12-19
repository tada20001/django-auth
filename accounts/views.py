from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.http import Http404
from django.utils.http import urlsafe_base64_decode

from django.views.generic import CreateView, UpdateView
#from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse_lazy
from .forms import SignupForm, ProfileForm
from .models import Profile

from django.contrib.auth.models import User

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


class ProfileUpdateView(UpdateView, LoginRequiredMixin):
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.profile

profile_edit = ProfileUpdateView.as_view()



class RequestLoginViaUrlView(PasswordResetView):
    template_name = 'accounts/request_login_via_url_form.html'
    title = '이메일을 통한 로그인'
    email_template_name = 'accounts/login_via_url.html'
    success_url = settings.LOGIN_URL


def login_via_url(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        current_user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
        raise Http404
    if default_token_generator.check_token(current_user, token):
        auth_login(request, current_user)
        messages.info(request, '로그인이 승인되었습니다.')
        return redirect('root')
    messages.error(request, '로그인이 거부되었습니다.')
    return redirect('root')


class MyPasswordChangeView(PasswordChangeView):
    template_name='accounts/password_change_form.html'
    success_url=reverse_lazy('profile')

    def form_valid(self, form):
        messages.info(self.request, '비밀번호 변경을 완료했습니다.')
        return super().form_valid(form)

class MyPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('login')
    email_template_name = 'accounts/password_reset_email.html'

    def form_valid(self, form):
        messages.info(self.request, '비밀번호 변경을 위한 링크를 이메일로 보내드렸습니다. 이메일을 확인해 주세요.')
        return super().form_valid(form)


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.info(self.request, '비밀번호가 재설정되었습니다.')
        return super().form_valid(form)
