from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class UserScores(models.Model):
    user = models.OneToOneField(User, related_name="scores", null=False)
    score_date = models.DateField(
        auto_now_add=True
    )
    cpm = models.IntegerField(
        default=0
    )
    mistakes = models.IntegerField(
        default=0
    )
    objects = models.Manager()

    def __str__(self):
        return self.user.username
