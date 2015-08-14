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
            '/play/multi/', {
                'user_input': 'good start',
                'opponent': 'someschmuck'
            }
        )
        self.assertEqual(response.content, 'off we go now')

    # Test 3
    # Check that /play/content/ page loads the correct content
    def test_content_api(self):
        response = Client().post(
            '/play/content2/',
            {
                'user': 'tpeek',
                'repo': 'Copy-n-Haste',
                'path': 'README.md'
            }
        )
        self.assertEqual(response.content[:25], 'A totally awesome website')


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

    # Test 4
    # Check playing single player game
    def test_single_player(self):
        self.login_helper(self.browser1, self.user1.username, 'abc')
        self.browser1.visit(
            '%s%s' % (self.live_server_url, '/play/')
        )
        time.sleep(2)
        snippet = self.browser1.find_by_id('type').value
        if snippet:
            snippet = snippet[:-(
                len(snippet.split()[-1]) + 1
            )]
            for c in snippet[:100]:
                self.browser1.type('typed', c)
                time.sleep(0.001)
        self.browser1.find_by_tag('input')[3].click()
        self.browser1.find_by_tag('input').last.click()
        self.assertEqual(
            self.browser1.url,
            '%s%s' % (self.live_server_url, '/scores/')
        )

    # # Test 5 - future consideration
    # # Check playing multiplayer game
    # def test_multiplayer(self):
    #     self.browser2 = Browser()
    #     self.login_helper(self.browser1, self.user1.username, 'abc')
    #     self.login_helper(self.browser2, self.user2.username, '123')
    #     self.browser1.find_by_tag('a')[2].click()

    #     time.sleep(2)
    #     self.browser2.find_by_tag('a')[2].click()

    #     time.sleep(2)

    #     snippet = self.browser1.find_by_id('type').value
    #     snippet = snippet[:-(len(snippet.split()[:-1]) + 1)]
    #     for i, c in enumerate(snippet):
    #         j = 2 * i
    #         self.browser1.type('typed', c)
    #         self.browser2.type('typed', snippet[j])
    #         time.sleep(0.001)
    #         self.browser2.type('typed', snippet[j + 1])
    #         time.sleep(0.001)

    #     self.assertEqual(self.browser1.find_by_id('result').text, 'loser')
    #     self.assertEqual(self.browser2.find_by_id('result').text, 'winner')

    #     self.browser2.quit()
