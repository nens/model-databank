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
from django.template import loader, Context
from django.utils.translation import ugettext_lazy as _

from autoslug import AutoSlugField

from lizard_auth_client.models import Organisation

from model_databank.vcs_utils import get_last_update_date
from model_databank.conf import settings  # to load app specific settings
from model_databank.db.fields import UUIDField

logger = logging.getLogger(__name__)

HG_LARGEFILES_EXTENSIONS = ('grd', 'tbl', 'asc', 'tif', 'sqlite')


def get_largefiles_file_paths(root_path):
    paths = []
    for root, dirs, files in os.walk(root_path):
        # skip .hg files
        if '/.hg' in root:
            continue
        for f in files:
            fn, ext = os.path.splitext(f)
            if ext and ext.startswith('.'):
                ext = ext[1:].lower()  # remove the dot
            if ext in HG_LARGEFILES_EXTENSIONS:
                paths.append(os.path.join(root, f))
    return paths


def add_hgignore_file(root_path):
    hgignore_path = os.path.join(root_path, '.hgignore')
    hgignore_file = open(hgignore_path, 'w')
    template = loader.get_template('model_databank/hgignore.txt')
    context = Context()
    hgignore_text = template.render(context)
    hgignore_file.write(hgignore_text)
    hgignore_file.close()


class ActiveModelReferenceManager(models.Manager):
    def get_query_set(self):
        return super(ActiveModelReferenceManager, self).get_query_set().filter(
            is_deleted=False)


class ModelType(models.Model):
    """ModelType is used in the ModelReference class to determine which type
    a model is, e.g.: 3Di, 3Di (urban), Sobek, etc.
    """
    name = models.CharField(verbose_name=_("name"), max_length=15, unique=True)
    slug = AutoSlugField(populate_from='name')

    class Meta:
        ordering = ('pk',)

    def __unicode__(self):
        return self.name


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

    owner = models.ForeignKey('auth.User', null=True)
    organisation = models.ForeignKey(Organisation, blank=True, null=True)

    type = models.ForeignKey(ModelType, null=True,
                             verbose_name=_("model type"))

    # TODO: identifier should be unique for team, not globally
    identifier = models.CharField(
        verbose_name=_("unique identifier"), max_length=200, unique=True)
    slug = AutoSlugField(populate_from='identifier')
    uuid = UUIDField()

    description = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    # last repo update is filled with a cronjob that runs every 15 minutes
    # check for the latest commit
    last_repo_update = models.DateTimeField(blank=True, null=True)

    is_deleted = models.BooleanField(default=False)  # handle by self.delete()

    objects = models.Manager()
    active = ActiveModelReferenceManager()

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
        return ('model_reference_detail', [self.slug])

    @property
    def symlink(self):
        """Symlink to the repository."""
        return os.path.join(settings.MODEL_DATABANK_SYMLINK_PATH, self.slug)

    @property
    def repository(self):
        """Repository path."""
        return os.path.join(settings.MODEL_DATABANK_DATA_PATH, self.uuid)

    @property
    def repository_url(self):
        """Return Mercurial repository URL."""
        url_root = settings.MODEL_DATABANK_REPOSITORY_URL_ROOT.strip('/')
        return '/'.join([url_root, self.slug])

    @property
    def repository_ssh_url(self):
        """Return Mercurial repository path. Can be used for cloning over
        SSH."""
        return "/".join([settings.MODEL_DATABANK_REPOSITORY_SSH_URL_ROOT,
                         self.symlink])

    @property
    def repository_files_url(self):
        """Return Mercurial URL that shows files page."""
        return '/'.join([self.repository_url, 'file'])

    @property
    def organisation_uuid(self):
        if self.organisation:
            return self.organisation.unique_id

    @property
    def model_type(self):
        if self.type:
            return self.type.slug

    def safe_delete(self, *args, **kwargs):
        """
        'Delete' this model reference while still being restorable by removing
        its symlink and setting the `is_deleted` field to True.

        Method can be used by end users. Deleting via the admin interface
        permanently and irreversibly deletes this instance.

        """
        if not self.is_deleted:
            try:
                os.unlink(self.symlink)
            except OSError:
                logger.exception(_("Failed to delete symlink: %s.") %
                                 self.symlink)
                raise
            else:
                self.is_deleted = True
                self.save()

    def restore(self, *args, **kwargs):
        """
        Restore this model reference by re-creating its symlink and setting
        the `is_deleted` field to False.

        """
        if self.is_deleted:
            try:
                os.symlink(self.repository, self.symlink)
            except OSError:
                logger.exception("Failed to create symlink. "
                                 "Could it be a Windows directory?")
                raise
            else:
                self.is_deleted = False
                self.save()

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        if self.type:
            return _("%(identifier)s (%(type)s)") % {
                'identifier': self.identifier, 'type': self.type.slug}
        else:
            return self.identifier


class ModelUpload(models.Model):
    # TODO: add upload_by field
    model_reference = models.ForeignKey(
        ModelReference, related_name='uploads', null=True)

    uploaded_by = models.ForeignKey('auth.User', null=True)
    organisation = models.ForeignKey(Organisation, blank=True, null=True)

    # identifier is used for new model files uploads
    identifier = models.CharField(
        verbose_name=_("unique identifier"), max_length=200, blank=True)
    description = models.TextField(blank=True)
    model_type = models.ForeignKey(ModelType, null=True,
                                   verbose_name=_("model type"))

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
            logger.exception("File is not a zip file: %s" % self.file_path)
            return
        except IOError:
            logger.exception("Zip file path probably not found.")
            return

        extract_to = os.path.join(
            settings.MODEL_DATABANK_ZIP_EXTRACT_PATH, str(self.id))
        z.extractall(path=extract_to)

        # create repo dir if not exist
        if not self.model_reference:
            # convert to hg repo
            os.chdir(extract_to)
            subprocess.call([settings.HG_CMD, 'init'])
            # add the .hgignore file
            add_hgignore_file(extract_to)
            # loop through files and add files from largefiles extensions
            largefiles_file_paths = get_largefiles_file_paths(extract_to)
            for fp in largefiles_file_paths:
                # this is needed even when a largefiles patterns entry
                # is added to ~/.hgrc
                subprocess.call([settings.HG_CMD, 'add', '--large', fp])
                logger.info("Added %s as large file to repository\n" % fp)

            subprocess.call([settings.HG_CMD, 'add'])
            subprocess.call([settings.HG_CMD, 'commit', '-m',
                             'Initial commit.', '--user', 'Model Databank'])
            # make it a bare repository (i.e. without a working copy)
            subprocess.call([settings.HG_CMD, 'update', 'null'])
            # if we got here, create a ModelReference with uuid for the
            # repo dir naming
            model_reference = ModelReference(
                type=self.model_type,
                owner=self.uploaded_by,
                identifier=self.identifier,
                description=self.description,
                organisation=self.organisation)
            model_reference.save()

            shutil.move(extract_to, model_reference.repository)

            # create symlink to the repository
            try:
                os.symlink(model_reference.repository,
                           model_reference.symlink)
            except OSError:
                logger.exception("Failed to create symlink for repository. "
                                 "Could it be a Windows directory?")
                # TODO: rollback?
                # Call model_reference.delete(), which should be overriden.
                # Override model_reference.delete() by setting `deleted`
                # boolean field to True. This is done for restoring purposes.
                # But perhaps in this case it should be deleted totally.
                # Perhaps by creating a model
                return
            else:
                self.model_reference = model_reference
                self.is_processed = True
                self.save()

                # set the last repo update date
                last_repo_update = get_last_update_date(model_reference)
                model_reference.last_repo_update = last_repo_update
                model_reference.save()

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
            return (_("%(model_reference)s (version: %(version)s "
                      "(parent: %(parent)s))") %
                    {'model_reference': self.model_reference.identifier,
                     'version': self.name, 'parent': self.parent.name})
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
