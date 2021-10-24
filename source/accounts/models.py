from django.core.validators import URLValidator
from django.db import models
from django.contrib.auth import get_user_model


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='profile', on_delete=models.CASCADE,
                                verbose_name='Profile')
    avatar = models.ImageField(null=True, blank=True, upload_to='user_pics', verbose_name='Avatar')
    github_url = models.CharField(max_length=300, verbose_name='Github', validators=[URLValidator])
    about = models.TextField(max_length=1000, verbose_name='About')

    def __str__(self):
        return self.user

