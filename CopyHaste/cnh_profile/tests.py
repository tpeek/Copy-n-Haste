#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
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


class UserNProfileTests(TransactionTestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user1.set_password('abc')
        self.user1.save()
        self.profile1 = self.user1.profile

    def tearDown(self):
        User.objects.all().delete()

    # Test 1
    # Check that a CNHProfile is created when user is created
    def test_create_profile(self):
        self.assertEqual(len(CNHProfile.objects.all()), 1)
        self.assertEqual(self.profile1.user.username, self.user1.username)

    # Test 2
    # Check that profile can accept empty string for nickname
    def test_blank_nickname(self):
        self.profile1.nickname = ''
        self.profile1.save()
        self.assertEqual(self.profile1.nickname, '')

    # Test 3
    # Check that profile can accept empty string for website
    def test_blank_website(self):
        self.profile1.website = ''
        self.profile1.save()
        self.assertEqual(self.profile1.website, '')

    # Test 4
    # Check that profile cannot accept string of length 129 for nickname
    def test_long_nickname(self):
        self.profile1.nickname = 'a' * 129
        with self.assertRaises(DataError):
            self.profile1.save()

    # Test 5
    # Check that profile can accept string of length 129 for website
    def test_long_website(self):
        self.profile1.website = 'a' * 129
        self.profile1.save()
        self.assertEqual(self.profile1.website, 'a' * 129)

    # Test 6
    # Check that is_active property works as expected
    def test_is_active(self):
        self.assertIs(self.user1.is_active, True)
        self.assertIs(self.profile1.is_active, True)

    # Test 7
    # Check that is_active can be changed
    def test_is_not_active(self):
        self.assertIs(self.profile1.is_active, True)
        self.profile1.user.is_active = False
        self.assertIs(self.profile1.is_active, False)

    # Test 8
    # Check that ActiveProfileManager works
    def test_active(self):
        self.assertIs(len(CNHProfile.active.all()), 1)
        self.profile1.user.is_active = False
        self.profile1.user.save()
        self.assertFalse(CNHProfile.active.all())

    # Test 9
    # Check that if user is killed, profile is killed
    def test_no_profile(self):
        self.assertIs(len(CNHProfile.objects.all()), 1)
        self.user1.delete()
        self.assertFalse(CNHProfile.objects.all())

    # Test 10
    # Check that if profile is killed, user is killed
    def test_no_user(self):
        self.assertIs(len(User.objects.all()), 1)
        self.profile1.delete()
        self.assertFalse(User.objects.all())

    # Test 11
    # Check string representation of profile
    def test_string_profile(self):
        self.assertEqual(str(self.profile1), self.user1.username)


# # # # # # # # # # # # #
# Web Tests for Profile #
# # # # # # # # # # # # #


@override_settings(DEBUG=True)
class UnAuthNWebTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(UnAuthNWebTests, cls).setUpClass()
        cls.browser = Browser()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(UnAuthNWebTests, cls).tearDownClass()

    # Test 12
    # Check anonymous get of /profile/
    def test_unauthn_get_profile(self):
        self.browser.visit('%s%s' % (self.live_server_url, '/profile/'))
        self.assertEqual(
            self.browser.url,
            '%s%s' % (self.live_server_url, '/accounts/login/?next=/profile/')
        )

    # Test 13 - future consideration
    # Check anonymous get of /profile/edit/
    # def test_unauthn_get_edit(self):
    #     self.browser.visit('%s%s' % (self.live_server_url, '/profile/edit/'))
    #     self.assertEqual(
    #         self.browser.url,
    #         '%s%s' % (self.live_server_url, '/accounts/login/?next=/profile/edit/')
    #     )


@override_settings(DEBUG=True)
class AuthNWebTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(AuthNWebTests, cls).setUpClass()
        cls.browser = Browser()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(AuthNWebTests, cls).tearDownClass()

    def setUp(self):
        self.user1 = UserFactory()
        self.user1.set_password('abc')
        self.user1.save()
        self.profile1 = self.user1.profile

        self.browser.visit('%s%s' % (self.live_server_url, '/accounts/login/'))
        self.browser.fill('username', self.user1.username)
        self.browser.fill('password', 'abc')
        self.browser.find_by_value('Log in').first.click()

    def tearDown(self):
        User.objects.all().delete()

    # Test 12
    # Check user get of /profile/
    def test_authn_get_profile(self):
        self.browser.visit('%s%s' % (self.live_server_url, '/profile/'))
        self.assertEqual(
            self.browser.url,
            '%s%s' % (self.live_server_url, '/profile/')
        )

    # Test 13
    # Check user get of /profile/edit/ and post updates - future consideration
    # def test_authn_edit(self):
    #     self.browser.visit('%s%s' % (self.live_server_url, '/profile/edit/'))
    #     self.assertEqual(
    #         self.browser.url,
    #         '%s%s' % (self.live_server_url, '/profile/edit/')
    #     )
