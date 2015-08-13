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


# # # # # # # # # # # # # #
# Client Tests for Views  #
# # # # # # # # # # # # # #


class PlayClientTests(TestCase):

    # Test 1
    # Check that /play/ page loads the correct template
    def test_play_template(self):
        response = Client().get('/play/')
        self.assertTemplateUsed(response, 'typingtest2.html')

    # Test 2
    # Check that /play/multi/ page loads the correct template
    def test_multi_template(self):
        response = Client().get('/play/multi/')
        self.assertTemplateUsed(response, 'typingtest3.html')

    # Test 3
    # Check that /play/content/ page loads the correct content
    def test_content_api(self):
        response = Client().post(
            '/play/content/',
            {
                'user': 'tpeek',
                'repo': 'Copy-n-Haste',
                'path': 'README.md'
            }
        )
        self.assertEqual(response.content[:14], '# Copy-n-Haste')
