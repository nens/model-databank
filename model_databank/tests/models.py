# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import os

from model_databank.conf import settings
from django.test import TestCase

from .factories import ModelReferenceFactory


class ExampleTest(TestCase):

    def test_something(self):
        self.assertEquals(1, 1)


class ModelGenerationTests(TestCase):

    def setUp(self):
        self.mfs = []
        for i in range(10):
            self.mfs.append(ModelReferenceFactory.stub())

    def test_number(self):
        self.assertEqual(len(self.mfs), 10)

    def test_symlink_path(self):
        mf = self.mfs[0]
        expected_path = os.path.join(settings.MODEL_DATABANK_SYMLINK_PATH,
                                     mf.slug)
        self.assertEqual(mf.symlink, expected_path)
