# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from django.test import TestCase

from .factories import UserFactory


class ModelReferenceListViewTests(TestCase):
    """Tests for the ModelReferenceListView."""
    def test_login(self):
        user = UserFactory.build()
        with self.settings(
                AUTHENTICATION_BACKENDS=[
                    'model_databank.tests.auth_mock.AuthBackend']):
            self.client.login(username=user.username)
            response = self.client.get('/')
            self.assertEqual(response.status_code, 302)
