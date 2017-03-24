from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


BRANCH_CHOICES = (
    ('B.Tech', 'B.Tech'),
    ('MCA', 'MCA'),
)

YEAR_CHOICES = (
    ('1st', '1st'),
    ('2nd', '2nd'),
    ('3rd', '3rd'),
    ('4th', '4th'),
    ('5th', '5th'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    regd_no = models.CharField(max_length=10, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    branch = models.CharField(choices=BRANCH_CHOICES, max_length=6, default='MCA')
    year = models.CharField(choices=YEAR_CHOICES, max_length=3, default='1st')
    phone = models.CharField(max_length=10, blank=True, null=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
