from .models import CNHProfile
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


@receiver(post_save, sender=User)
def create_user_profile(sender, **kwargs):
    """A User should always have an CNHProfile"""
    instance = kwargs.get('instance')
    if not instance or kwargs.get('raw', False):
        return
    try:
        instance.profile
    except CNHProfile.DoesNotExist:
        instance.profile = CNHProfile()
        instance.profile.save()


@receiver(post_delete, sender=CNHProfile)
def rm_user_profile(sender, **kwargs):
    """If an CNHProfile is deleted, delete it's User too"""
    instance = kwargs.get('instance')
    if not instance:
        return
    instance.user.delete()
