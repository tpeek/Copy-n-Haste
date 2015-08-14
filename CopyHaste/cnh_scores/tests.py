#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TransactionTestCase
from django.test.utils import override_settings
import factory
from faker import Faker
from splinter import Browser
from .models import UserScores, Matches


faker = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda x: faker.username())
    email = factory.LazyAttribute(lambda x: faker.email())


# # # # # # # # # # # # #
# Unit Tests for Models #
# # # # # # # # # # # # #


class UserScoresNMatchesTests(TransactionTestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user1.set_password('abc')
        self.user1.save()

        self.user2 = UserFactory.build()
        self.user2.set_password('123')
        self.user2.save()

        self.userscore1 = UserScores(user=self.user1)
        self.userscore1.save()

        self.userscore2 = UserScores(user=self.user2)
        self.userscore2.save()

        self.match1 = Matches(winner=self.userscore1, loser=self.userscore2)
        self.match1.save()

    # Test 1
    # Check that a related name is created for the user for UserScore
    def test_user_for_userscore(self):
        self.assertEqual(self.user1.scores.all()[0], self.userscore1)

    # Test 2
    # Check for database error if no user specified
    def test_error_for_userscore(self):
        self.userscore3 = UserScores()
        with self.assertRaises(IntegrityError):
            self.userscore3.save()

    # Test 3
    # Check that a date is created for UserScore
    def test_date_for_userscore(self):
        self.assertTrue(self.userscore1.score_date)

    # Test 4
    # Check string representation for UserScore
    def test_str_for_userscore(self):
        self.assertEqual(str(self.userscore1), self.userscore1.score_date)

    # Test 5
    # Check that related names are created for users for Matches
    def test_users_for_matches(self):
        self.assertEqual(self.userscore1.winner.all()[0], self.match1)
        self.assertEqual(self.userscore2.loser.all()[0], self.match1)

    # Test 6
    # Check for database error if no loser specified
    def test_error_for_matches(self):
        self.match2 = Matches(winner=self.userscore2)
        with self.assertRaises(IntegrityError):
            self.match2.save()

    # Test 7
    # Check that a date is created for Matches
    def test_date_for_matches(self):
        self.assertTrue(self.match1.score_date)

    # Test 8
    # Check string representation for Matches
    def test_str_for_matches(self):
        self.assertEqual(
            str(self.match1),
            "Winner:" + str(self.user1) + " Loser:" + str(self.user2)
        )


# # # # # # # # # # # # # #
# Client Tests for Views  #
# # # # # # # # # # # # # #


class MultiplayerClientTests(TestCase):

    # Test 9
    # Check that /scores/ page loads the correct template
    def test_scores_template(self):
        pass

    # Test 10
    # Check that /scores/result page loads the correct template
    def test_result_template(self):
        pass

    # Test 11
    # Check that /scores/match_score page loads the correct template
    def test_match_template(self):
        pass


# # # # # # # # # # # # # # #
# Web Tests for Multiplayer #
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

        self.scores1 = UserScores(
            user=self.user1,
            wpm_gross=110,
            wpm_net=100,
            mistakes=8
        )
        self.scores1.save()

        self.scores2 = UserScores(
            user=self.user2,
            wpm_gross=100,
            wpm_net=90,
            mistakes=10
        )
        self.scores2.save()

        self.match = Matches(winner=self.user1, loser=self.user2)
        self.match.save()

        self.browser = Browser()

    def tearDown(self):
        self.browser.quit()

    def login_helper(self, username, password):
        self.browser.visit(
            '%s%s' % (self.live_server_url, '/accounts/login/')
        )

        self.browser.fill('username', username)
        self.browser.fill('password', password)
        self.browser.find_by_value('Log in').first.click()

    # Test 12
    # Check anon get of /scores/
    def test_anon_get_scores(self):
        pass

    # Test 13
    # Check anon get of /scores/match_score
    def test_anon_get_match_score(self):
        pass

    # Test 14
    # Check scores for user
    def test_user_for_scores(self):
        self.login_helper(self.user1, 'abc')

    # Test 15
    # Check matches for user
    def test_user_for_matches(self):
        self.login_helper(self.user1, 'abc')
