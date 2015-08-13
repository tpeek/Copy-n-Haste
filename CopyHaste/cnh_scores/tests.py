#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.test import TestCase
from django.db import DataError
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TransactionTestCase
from django.test.utils import override_settings
import factory
from faker import Faker
from splinter import Browser
from .models import CNHProfile


fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = fake.username()
    email = fake.email()


# # # # # # # # # # # # #
# Unit Tests for Models #
# # # # # # # # # # # # #
