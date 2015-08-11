#!/usr/bin/env python


# from __future__ import unicode_literals
from django.db import DataError
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from django.core.urlresolvers import reverse
from django.test import TestCase
import factory
from faker import Faker
from splinter import Browser
# from time import sleep
from .models import CNHProfile


fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = fake.user_name()
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()


# # # # # # # # # # # # #
# Unit Tests for Models #
# # # # # # # # # # # # #


class UserNProfileTest(TestCase):
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
    # Check that profile can accept empty string for website_url
    def test_blank_website_url(self):
        self.profile1.website_url = ''
        self.profile1.save()
        self.assertEqual(self.profile1.website_url, '')

    # Test 4
    # Check that profile cannot accept string of length 129 for nickname
    def test_long_nickname(self):
        self.profile1.nickname = 'a' * 129
        with self.assertRaises(DataError):
            self.profile1.save()

    # Test 5
    # Check that profile can accept string of length 129 for website_url
    def test_long_website_url(self):
        self.profile1.website_url = 'a' * 129
        self.profile1.save()
        self.assertEqual(self.profile1.website_url, 'a' * 129)

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
        self.assertEqual(str(self.profile1), self.user1.get_full_name())


class UserProfileTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user1.set_password('secret')
        self.user1.save()
        self.profile1 = self.user1.profile
        self.client = Client()

    def tearDown(self):
        User.objects.all().delete()

    def test_user1_profile_view_self(self):
        self.client.login(
            username=self.user1.username, password='secret'
        )
        response = self.client.get(reverse('profile:detail'))
        self.assertContains(response, self.user1.email)
        self.assertContains(response, self.user1.username)

    def test_user1_profile_update_view_self(self):
        self.client.login(
            username=self.user1.username, password='secret'
        )
        response = self.client.get(reverse('profile:edit'))
        self.assertContains(response, self.user1.username)
        self.assertContains(response, self.user1.email)

    def test_user1_profile_update_post_self(self):
        self.client.login(
            username=self.user1.username, password='secret'
        )
        new_data = {
            'username': self.user1.username,
            'first_name': '',
            'last_name': '',
            'email': 'new@example.com',
            'camera': 'Super Nikon',
            'address': '123 Anywhere Dr',
            'web_url': 'http://www.example.com',
            'type_photography': 'existential'
        }
        response = self.client.post(
            reverse('profile:edit'), new_data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('profile:detail'))
        for key in new_data:
            self.assertContains(response, new_data[key])


class LiveServerSplinterTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(LiveServerSplinterTest, cls).setUpClass()
        cls.browser = Browser()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(LiveServerSplinterTest, cls).tearDownClass()
        sleep(3)

    def setUp(self):
        self.user1 = UserFactory(
            username='john',
            email='john@example.com',
            first_name='John',
            last_name='Stephenson'
        )
        self.user1.set_password('abc')
        self.user1.save()

    def login_helper(self, username, password):
        self.browser.visit('{}{}'.format(
            self.live_server_url, '/accounts/login/')
        )

        self.browser.fill('username', username)
        self.browser.fill('password', password)
        self.browser.find_by_value('Log in').first.click()

    def test_non_auth_profile_redirect(self):
        self.browser.visit('{}{}'.format(self.live_server_url, '/profile'))
        self.assertEqual(
            self.browser.url, '{}{}'.format(
                self.live_server_url, '/accounts/login/?next=/profile/'
            )
        )

    def test_non_auth_edit_profile_redirect(self):
        self.browser.visit('{}{}'.format(
            self.live_server_url, '/profile/edit')
        )
        self.assertEqual(
            self.browser.url, '{}{}'.format(
                self.live_server_url, '/accounts/login/?next=/profile/edit/'
            )
        )
