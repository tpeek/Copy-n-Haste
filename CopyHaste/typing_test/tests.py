#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.test import TestCase, Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
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
    # Check that /play/match/ page loads the correct template
    def test_match_template(self):
        response = Client().get('/play/match/')
        self.assertTemplateUsed(response, 'typingtest3.html')

    # Test 4
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


# # # # # # # # # # # # # # #
# Web Tests for Play Pages  #
# # # # # # # # # # # # # # #


@override_settings(DEBUG=True)
class PlayPagesWebTests(StaticLiveServerTestCase):

    def setUp(self):
        self.user1 = UserFactory.build()
        self.user1.set_password('abc')
        self.user1.save()
        self.browser = Browser()

    def tearDown(self):
        self.browser.quit()

    def login_helper(self, username, password):
        self.browser.visit('%s%s' % (self.live_server_url, '/accounts/login/'))

        self.browser.fill('username', username)
        self.browser.fill('password', password)
        self.browser.find_by_value('Log in').first.click()

    # Test 5
    # Check for anonymous playing single player game
    def test_anon_single_player(self):
        self.browser.visit(
            '%s%s' % (self.live_server_url, '/play/')
        )

    # Test 6
    # Check for anonymous playing multiplayer game
    def test_anon_multiplayer(self):
        pass

    # Test 7
    # Check for user playing single player game
    def test_user_single_player(self):
        pass

    # Test 8
    # Check for user playing multiplayer game
    def test_user_multiplayer(self):
        pass
