# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from django.contrib.auth.models import User

import factory

from model_databank import models


class ModelReferenceFactory(factory.DjangoModelFactory):
    """ModelReference factory.

    Can generate many ModelReference instances in a for loop, for example.

    """
    FACTORY_FOR = models.ModelReference

    identifier = factory.Sequence(lambda n: 'model {0}'.format(n))
    slug = factory.Sequence(lambda n: 'slug_{0}'.format(n))


class VersionFactory(factory.DjangoModelFactory):
    """Version factory."""
    FACTORY_FOR =  models.Version

    name = factory.Sequence(lambda n: 'version {0}'.format(n))


class VariantFactory(factory.DjangoModelFactory):
    """Variant factory."""
    FACTORY_FOR = models.Variant

    name = factory.Sequence(lambda n: 'variant {0}'.format(n))


class UserFactory(factory.DjangoModelFactory):
    """Factory for User"""
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: 'user_{0}'.format(n))
