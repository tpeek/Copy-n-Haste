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
    # Check that home page loads the correct template
    def test_home_template(self):
        response = Client().get('/')
        self.assertTemplateUsed(response, 'home.html')


# # # # # # # # # # # # # #
# Web Tests for Home Page #
# # # # # # # # # # # # # #


@override_settings(DEBUG=True)
class HomePageWebTests(StaticLiveServerTestCase):

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

    # Test 2
    # Check for login link from anonymous get of homepage
    def test_anon_login(self):
        self.browser.visit('%s%s' % (self.live_server_url, '/'))
        login_link = self.browser.find_by_tag('a')[3]
        self.assertEqual(
            '%s%s' % (self.live_server_url, '/accounts/login/'),
            login_link['href']
        )

    # Test 3
    # Check for register link from anonymous get of homepage
    def test_anon_register(self):
        self.browser.visit('%s%s' % (self.live_server_url, '/'))
        register_link = self.browser.find_by_tag('a')[4]
        self.assertEqual(
            '%s%s' % (self.live_server_url, '/accounts/register/'),
            register_link['href']
        )

    # Test 4
    # Check for user login success
    def test_login_success(self):
        self.login_helper(self.user1.username, 'abc')

        self.assertEqual(
            self.browser.url,
            '%s%s' % (self.live_server_url, '/profile/')
        )
        logout_link = self.browser.find_by_tag('a')[4]
        self.assertEqual(
            '%s%s' % (self.live_server_url, '/accounts/logout/?next=/'),
            logout_link['href']
        )
        greeting = self.browser.find_by_tag('big')[0]
        self.assertEqual(
            '%s%s%s' % ('Well howdy there, ', self.user1.username, '.'),
            greeting.text
        )

    # Test 5
    # Check for user logout success
    def test_logout_success(self):
        self.login_helper(self.user1.username, 'abc')

        self.browser.find_by_tag('a')[4].click()

        self.assertEqual(
            self.browser.url,
            '%s%s' % (self.live_server_url, '/')
        )

    # Test 6
    # Register brand new user
    def test_registration(self):
        self.browser.visit(
            '%s%s' % (self.live_server_url, '/accounts/register/')
        )

        self.browser.fill('username', 'joseph')
        self.browser.fill('email', 'joe@example.com')
        self.browser.fill('password1', '123')
        self.browser.fill('password2', '123')
        self.browser.find_by_value('Submit').first.click()

        self.assertEqual(
            self.browser.url,
            '%s%s' % (self.live_server_url, '/accounts/register/complete/')
        )

        link_end = mail.outbox[0].body.split('days:')[1].split()[0][18:]
        link = '%s%s' % (self.live_server_url, link_end)
        self.browser.evaluate_script('document.location="%s"' % link)
        self.assertEqual(
            self.browser.url,
            '%s%s' % (self.live_server_url, '/accounts/activate/complete/')
        )
        self.login_helper('joseph', '123')
        greeting = self.browser.find_by_tag('big')[0]
        self.assertEqual('Well howdy there, joseph.', greeting.text)
