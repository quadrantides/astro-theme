# coding=utf-8
"""
Created on 2020, May 14th
@author: orion
"""
from django.test import TestCase
from datetime import datetime, timedelta
from theme.models import HousesSystem


class HousesSystemTests(TestCase):
    def test_contents(self):
        """
        """

        all = HousesSystem.objects.all()
        print('ok')

        # self.assertEqual(futur_article.est_recent(), False)