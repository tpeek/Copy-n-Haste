from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


class ActiveProfileManager(models.Manager):
    def get_queryset(self):
        return super(ActiveProfileManager,
                     self).get_queryset().filter(user__is_active=True)


@python_2_unicode_compatible
class CNHProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", null=False)
    nickname = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        help_text='What is your nickname'
    )
    website = models.URLField(
        blank=True,
        help_text='What is your website URL?'
    )
    objects = models.Manager()
    active = ActiveProfileManager()

    def __str__(self):
        return self.user.username

    @property
    def is_active(self):
        return self.user.is_active
