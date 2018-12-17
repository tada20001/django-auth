from django.conf import settings
from django.db.models.signals import post_save
from django.db import models



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    website_url = models.URLField(blank=True)

    def __str__(self):
        return self.user.username

# 회원가입과 동시에 유저 객체를 만들어내기 때문에 유저 객체를 통해 프로파일 만들기
def on_post_save_for_user(sender, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        Profile.objects.create(user=user)

post_save.connect(on_post_save_for_user, sender=settings.AUTH_USER_MODEL)
