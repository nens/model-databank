# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.db import models
from django.utils.translation import ugettext_lazy as _

from autoslug import AutoSlugField

from model_databank.conf import settings  # to load app specific settings


class ModelReference(models.Model):
    """
    Work in progress. Mainly sketching to get a feel with the whole matter.

    Considerations
    --------------
    - Model naming: naming this class 'Model' is a no go, since the confusion
      it might give with django.db.models.Model.
    - Since it is mainly a reference to either a path or some metadata, we now
      chose to name it ModelReference. Other more or less viable ideas were
      ModelData, ModelInfo, ModelWrapper.

    - Metadata:

      In flooding relevant information about the different models is stored in
      the model itself; e.g. the SobekModel class has lots of fields that
      defines a Sobek model. A ThreediModel is merely a pointer to the mdu
      filename and to the scenario zip file name.

      To make this more flexible one idea is to make this class very compact
      and to add metadata about it in a document-based database, for example
      something like MongoDB.

      In order to make this work we somehow need a way to add and edit this
      (MongoDB) metadata document through some kind of admin page wrapping
      that document.

    - File path convention:

      To determine the file path automatically and flexibly (still being able
      to change project names for example), it is probably best to used
      project-, model-, version- and variant- ids, for example:

      For original model files:
      <PROJECT_DIR>/<project_id>/<model_id>/*

      For version files:
      <PROJECT_DIR>/<project_id>/<model_id>/_versions/<version_id>/*

      For variant (variant of a version) files:
      <PROJECT_DIR>/<project_id>/<model_id>/_versions/<version_id>/_variants/\
      <variant_id>/*

    """
    MODEL_TYPE_CHOICES = (
        (1, 'Sobek'),
        (2, '3Di'),
    )

    model_type = models.IntegerField(
        verbose_name=_("model type"), choices=MODEL_TYPE_CHOICES)

    identifier = models.CharField(
        verbose_name=_("unique identifier"), max_length=200, unique=True)
    slug = AutoSlugField(populate_from='identifier')

    comment = models.CharField(max_length=255, blank=True)

    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        model_type = dict(self.MODEL_TYPE_CHOICES)[self.model_type]
        return _("%(identifier)s (%(type)s model)") % {
            'identifier': self.identifier, 'type': model_type}


class Project(models.Model):
    """Project belonging to an owner."""
    owner = models.ForeignKey('auth.User')
    # name should be unique for owner
    name = models.CharField(verbose_name=_("name"), max_length=100)
    comment = models.CharField(verbose_name=_("comment"), max_length=255,
                               blank=True)
    slug = AutoSlugField(populate_from='name')
    model_references = models.ManyToManyField(ModelReference,
                                              related_name='provider')

    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return _("%(name)s (owner: %(owner)s)") % {'name': self.name,
                                                   'owner': self.owner}


class Version(models.Model):
    """Version of a model."""
    # specific model reference for this version
    # model can be null if parent is not null
    model = models.ForeignKey(ModelReference, related_name='versions',
                              null=True)
    parent = models.ForeignKey('self', null=True)
    name = models.CharField(verbose_name=_("name"), max_length=100)
    comment = models.CharField(verbose_name=_("comment"), max_length=255,
                               blank=True)

    created = models.DateTimeField(auto_now_add=True)


class Variant(models.Model):
    """Variant of a version."""
    # version this variant is based on
    version = models.ForeignKey('Version', related_name='variants')
    name = models.CharField(verbose_name=_("name"), max_length=100)
    comment = models.CharField(max_length=255, blank=True)

    created = models.DateTimeField(auto_now_add=True)
