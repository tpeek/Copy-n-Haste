#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.test import TestCase, Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.core import mail
from django.test.utils import override_settings
import factory
from faker import Faker
from splinter import Browser


fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = fake.username()
    email = fake.email()


# # # # # # # # # # # # # # # #
# Client Tests for Templates  #
# # # # # # # # # # # # # # # #


class HomepageClientTests(TestCase):

    # Test 1
    # Check that /game/ page loads the correct template
    def test_game_template(self):
        response = Client().get('/game/')
        self.assertTemplateUsed(response, 'typingtest2.html')

    # Test 2
    # Check that /game/multi/ page loads the correct template
    def test_multi_template(self):
        response = Client().get('/game/multi/')
        self.assertTemplateUsed(response, 'typingtest3.html')

    # Test 3
    # Check that /game/content/ page loads the correct content
    def test_home_template(self):
        response = Client().get('/game/content/')
        import pdb; pdb.set_trace()
