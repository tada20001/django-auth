from django.conf import settings
#from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.models import AbstractUser

from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.db import models

from django.contrib.auth.models import UserManager as AuthUserManager
# Proxy User Model exmaple
# class User(AuthUser):
#     class Meta:
#         proxy = True
#
#     @property
#     def name(self):
#         return '{} {}'.format(self.last_name, self.first_name)

# AbstractUser 상속을 통한 유저모델 커스텀

class UserManager(AuthUserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('sex', 'm') # sex필드에 대한 디폴트값 지정
        return super().create_superuser(username, email, password, **extra_fields)

class User(AbstractUser):
    sex = models.CharField(
            max_length=1,
            choices=(
                    ('f', 'female'),
                    ('m', 'male')),
            verbose_name='성별')
    objects = UserManager()


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    website_url = models.URLField(blank=True)

    def __str__(self):
        return self.user.username

# 회원가입과 동시에 유저 객체를 만들어내기 때문에 유저 객체를 통해 프로파일 만들기
def on_post_save_for_user(sender, **kwargs):
    if kwargs['created']:
        # 1. 유저가입 시기
        user = kwargs['instance']
        Profile.objects.create(user=user)

        # 2. 환영 이메일 보내기 : 동기적으로 작동
        send_mail(
            '환영합니다.',
            '가입을 축하합니다.',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
            )

post_save.connect(on_post_save_for_user, sender=settings.AUTH_USER_MODEL)
