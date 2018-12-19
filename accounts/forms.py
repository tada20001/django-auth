from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from .models import User, Profile
from django import forms


class SignupForm(UserCreationForm):
    sex = forms.ChoiceField(required=True, choices=(
            ('f', 'female'),
            ('m', 'male')))
    bio = forms.CharField(required=False)
    website_url = forms.URLField(required=False)

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
        self.fields['username'].help_text = 'Enter Email Format.'
        self.fields['username'].label = 'Email'
        self.fields['sex'].label = '성별'

    def save(self):
        user = super().save(commit=False)
        user.email = user.username
        user.sex = self.cleaned_data.get('sex')
        user.save()

        bio = self.cleaned_data.get('bio')
        website_url = self.cleaned_data.get('website_url')

        Profile.objects.create(user=user, bio=bio, website_url=website_url) # 회원가입 내용 프로필에 반영

        return user

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('bio', 'website_url')



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'website_url']
