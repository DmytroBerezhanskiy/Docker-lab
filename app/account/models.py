from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    telephone = models.CharField(max_length=12, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    birthday = models.DateField(blank=True, null=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
