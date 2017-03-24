from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=10)
    birth_date = models.DateField(null=True, blank=True)
    branch = models.CharField(choices=BRANCH_CHOICES, max_length=6)
    year = models.CharField(choices=YEAR_CHOICES, max_length=3)
    phone = models.CharField(max_length=10, default='')


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
