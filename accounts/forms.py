from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from django import forms


class SignupForm(UserCreationForm):
    # 로그인 아이디를 이메일로 사용하기

    # 1. 첫번째 방법 : username에 대한  validators, clean_필드명
    # def clean_username(self):
    #     value = self.cleaned_date.get('username')
    #     if value:
    #         validate_email(value)
    #     return value

    # 2. 두번째 방법
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].validators = [validate_email]
        self.fields['username'].help_text = 'Enter email format'
        self.fields['username'].label = _('Email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = user.username
        if commit:
            user.save()
        return user
