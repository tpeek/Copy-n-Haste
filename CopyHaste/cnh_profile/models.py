from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


class ActiveProfileManager(models.Manager):
    def get_queryset(self):
        return super(ActiveProfileManager,
                     self).get_queryset().filter(user__is_active=True)


@python_2_unicode_compatible
class CNHProfile(models.Model):
    nickname = models.CharField(max_length=128, null=True, blank=True)
    user = models.OneToOneField(User, related_name="profile")
    website_url = models.URLField(null=True, blank=True)
    objects = models.Manager()
    active = ActiveProfileManager()

    def __str__(self):
        return self.nickname or self.user.get_full_name() or self.user.username

    @property
    def is_active(self):
        return self.user.is_active
