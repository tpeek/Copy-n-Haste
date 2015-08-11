from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class UserScores(models.Model):
    user = models.ForeignKey(User, related_name="scores", default=None, null=False)
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
        return str(self.score_date)


class Matches(models.Model):
    match_date = models.DateTimeField(auto_now_add=True)
    winner = models.ForeignKey(UserScores, related_name="winner", default=None, null=False)
    loser = models.ForeignKey(UserScores, related_name="loser", default=None, null=False)
    objects = models.Manager()

    def __str__(self):
        return str("Winner:" + str(self.winner.user) + " Loser:" + str(self.loser.user))
