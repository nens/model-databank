# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import subprocess
import os
import shutil
import zipfile
import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from autoslug import AutoSlugField

from model_databank.conf import settings  # to load app specific settings
from model_databank.db.fields import UUIDField

logger = logging.getLogger(__name__)

HG_LARGEFILES_EXTENSIONS = ('grd', 'tbl', 'asc')


def get_largefiles_file_paths(root_path):
    paths = []
    for root, dirs, files in os.walk(root_path):
        # skip .hg files
        if '/.hg' in root:
            continue
        for f in files:
            if f[-3:].lower() in HG_LARGEFILES_EXTENSIONS:
                paths.append(os.path.join(root, f))
    return paths


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
    SOBEK_MODEL_TYPE_ID = 1
    THREEDI_MODEL_TYPE_ID = 2
    MODEL_TYPE_CHOICES = (
        (SOBEK_MODEL_TYPE_ID, 'Sobek'),
        (THREEDI_MODEL_TYPE_ID, '3Di'),
    )

    # TODO: consider renaming model_type, possible options: type, ?
    model_type = models.IntegerField(
        verbose_name=_("model type"), choices=MODEL_TYPE_CHOICES)

    identifier = models.CharField(
        verbose_name=_("unique identifier"), max_length=200, unique=True)
    slug = AutoSlugField(populate_from='identifier')
    uuid = UUIDField()

    comment = models.CharField(max_length=255, blank=True)

    created = models.DateTimeField(auto_now_add=True)

    @property
    def path(self):
        if self.uuid:
            return os.path.join(settings.MODEL_DATABANK_DATA_PATH,
                                str(self.uuid))
        else:
            # created with Factory.build for example
            return None

    def create_version(self, name, comment=None):
        versions = self.versions
        if not versions:
            version = Version(model_reference=self, name=name, comment=comment)
            version.save()
            print("successfully saved version: %s" % version)
            # TODO: log instead of print
            return version
        else:
            # get latest version if any
            latest_version = versions[0]
            version = Version(parent=latest_version, name=name,
                              comment=comment)
            version.save()
            print("successfully saved version: %s" % version)
            # TODO: log instead of print
            return version

    @models.permalink
    def get_absolute_url(self):
        return ('model_reference_detail', [str(self.id)])

    @property
    def model_type_str(self):
        return dict(self.MODEL_TYPE_CHOICES)[self.model_type]

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        model_type = dict(self.MODEL_TYPE_CHOICES)[self.model_type]
        return _("%(identifier)s (%(type)s model)") % {
            'identifier': self.identifier, 'type': model_type}


class ModelUpload(models.Model):
    # TODO: add upload_by field
    model_reference = models.ForeignKey(
        ModelReference, related_name='uploads', null=True)

    # identifier is used for new model files uploads
    identifier = models.CharField(
        verbose_name=_("unique identifier"), max_length=200, blank=True)
    description = models.TextField(blank=True)

    file_path = models.FilePathField(max_length=255)

    is_processed = models.BooleanField(default=False)

    uploaded = models.DateTimeField(auto_now_add=True)

    def process(self):
        if self.is_processed:
            logger.error("Already processed %s." % self)
            return
        try:
            z = zipfile.ZipFile(self.file_path)
        except zipfile.BadZipfile:
            logger.error("File is not a zip file: %s\n" %
                         self.file_path)
            return
        except IOError, msg:
            logger.error("%s\n" % msg)
            return

        extract_to = os.path.join(
            settings.MODEL_DATABANK_ZIP_EXTRACT_PATH, str(self.id))
        z.extractall(path=extract_to)

        # create repo dir if not exist
        if not self.model_reference:
            # convert to hg repo
            os.chdir(extract_to)
            subprocess.call([settings.HG_CMD, 'init'])
            # loop through files and add files from largefiles extensions
            largefiles_file_paths = get_largefiles_file_paths(extract_to)
            for fp in largefiles_file_paths:
                # this is needed even when a largefiles patterns entry
                # is added to ~/.hgrc
                subprocess.call([settings.HG_CMD, 'add', '--large', fp])
                logger.info("Added %s as large file to repository\n" % fp)

            subprocess.call([settings.HG_CMD, 'add'])
            subprocess.call([settings.HG_CMD, 'commit', '-m',
                             'Initial commit.'])
            # if we got here, create a ModelReference with uuid for the
            # repo dir naming
            model_reference = ModelReference(
                # for now, assume 3Di
                model_type=ModelReference.THREEDI_MODEL_TYPE_ID,
                identifier=self.identifier,
                comment=self.description)
            model_reference.save()

            repo_dir = os.path.join(settings.MODEL_DATABANK_DATA_PATH,
                str(model_reference.uuid))
            shutil.move(extract_to, repo_dir)

            self.model_reference = model_reference
            self.is_processed = True
            self.save()
            return self


def __unicode__(self):
        if self.model_reference:
            return _("Upload for %(model)s (%(path)s)") % {
                'model': self.model_reference, 'path': self.file_path
            }
        return _("New model upload (%(path)s)") % {'path': self.file_path}


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
    # model_reference can be null if parent is not null
    # equals a tag in DVCS; an approved release
    model_reference = models.ForeignKey(
        ModelReference, related_name='versions', null=True)
    # TODO: consider not using parent but vcs_commit or vcs_tag field
    parent = models.ForeignKey('self', null=True)
    name = models.CharField(verbose_name=_("name"), max_length=100)
    comment = models.CharField(verbose_name=_("comment"), max_length=255,
                               blank=True)

    # TODO: add `approved` field or use tag to determine whether a commit
    # is approved

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        if self.parent:
            return _("%(model_reference)s (version: %(version)s "
                     "(parent: %(parent)s))") % {
                'model_reference': self.model_reference.identifier,
                'version': self.name, 'parent': self.parent.name}
        else:
            return _("%(model_reference)s (version: %(version)s)") % {
                'model_reference': self.model_reference.identifier,
                'version': self.name
            }


class Variant(models.Model):
    """Variant of a version."""
    # version this variant is based on
    version = models.ForeignKey('Version', related_name='variants')
    name = models.CharField(verbose_name=_("name"), max_length=100)
    comment = models.CharField(max_length=255, blank=True)

    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return _("%(version)s - variant: %(variant)s") % {
            'version': self.version, 'variant': self.name
        }
