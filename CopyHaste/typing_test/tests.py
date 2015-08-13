#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.test import TestCase, Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.test.utils import override_settings
import factory
from faker import Faker
import redis
from splinter import Browser
import time


faker = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda x: faker.username())
    email = factory.LazyAttribute(lambda x: faker.email())


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
    # Check that /play/multi/ page loads the correct content
    def test_multi_template(self):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.getset('', 'begin')   # anon username is empty string
        r.getset('someschmuck', 'off we go now')
        response = Client().post(
            '/play/multi/',
            {
                'user_input': 'good start',
                'opponent': 'someschmuck'
            }
        )
        self.assertEqual(response.content, 'off we go now')

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

        self.user2 = UserFactory.build()
        self.user2.set_password('123')
        self.user2.save()

        self.browser1 = Browser()

    def tearDown(self):
        self.browser1.quit()

    def login_helper(self, browser, username, password):
        browser.visit(
            '%s%s' % (self.live_server_url, '/accounts/login/')
        )

        browser.fill('username', username)
        browser.fill('password', password)
        browser.find_by_value('Log in').first.click()

    # Test 5
    # Check perfectly playing single player game
    def test_perfect_single_player(self):
        self.browser1.visit(
            '%s%s' % (self.live_server_url, '/play/')
        )
        start = time.time()
        snippet = self.browser1.find_by_id('type').value
        for c in snippet:
            self.browser1.type('typed', c)
            time.sleep(0.1)
        elapsed = time.time() - start
        wpm = str(len(snippet.split()) / (elapsed / 60))
        accuracy = '100 %'
        self.assertEqual(self.browser1.find_by_id('stat_wpm').text, wpm)
        self.assertEqual(self.browser1.find_by_id('stat_score').text, accuracy)

    # Test 6
    # Check terribly playing single player game
    def test_crappy_single_player(self):
        self.browser1.visit(
            '%s%s' % (self.live_server_url, '/play/')
        )
        snippet = self.browser1.find_by_id('type').value
        start = time.time()
        for word in snippet.split():
            self.browser1.type('typed', 'aaaa ')
            time.sleep(0.1)
        elapsed = time.time() - start
        wpm = str(int(len(snippet.split()) / (elapsed / 60)))
        accuracy = '0 %'
        self.assertEqual(self.browser1.find_by_id('stat_wpm').text, wpm)
        self.assertEqual(self.browser1.find_by_id('stat_score').text, accuracy)

    # Test 7
    # Check playing multiplayer game
    def test_multiplayer(self):
        self.browser2 = Browser()
        self.login_helper(self.browser1, self.user1.username, 'abc')
        self.login_helper(self.browser2, self.user2.username, '123')

        self.browser1.visit(
            '%s%s' % (self.live_server_url, '/play/')
        )
        snippet = self.browser1.find_by_id('type').value
        for c in snippet:
            self.browser1.type('typed', c)
            time.sleep(0.1)

        self.browser2.quit()
