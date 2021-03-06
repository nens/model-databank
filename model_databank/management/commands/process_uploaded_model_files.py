import os
import sys
import datetime
import random
import shutil
import string
import time

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from lizard_auth_client.models import Organisation

from model_databank.models import ModelUpload, ModelReference, ModelType


def random_str(n):
    """
    A further improvement, using an existing
    library attribute.
    """
    out_str = ""
    for i in xrange(n):
        out_str += random.choice(string.ascii_lowercase)
    return out_str


def get_ftp_user(username='ftp', password=None):
    try:
        return User.objects.get(username=username)
    except ObjectDoesNotExist:
        password = password or random_str(32)
        return User.objects.create_user(username=username, password=password,
                                        email='f@f.nl')


class Command(BaseCommand):
    help = 'Process the uploaded unprocessed model zip files.'

    def handle(self, *args, **options):
        # Check whether there are zip files in the
        # MODEL_DATABANK_FTP_UPLOAD_PATH and put them in the regular upload
        # directory and create a ModelUpload instance of them, so the can be
        # processed.
        ftp_upload_path = getattr(settings, 'MODEL_DATABANK_FTP_UPLOAD_PATH',
                                  None)
        if not ftp_upload_path:
            sys.stdout.write(
                "No MODEL_DATABANK_FTP_UPLOAD_PATH in settings.\n")
        else:
            # get all zipfiles; return absolute paths to zipfiles
            # directory the zipfile is in, should be the organisation name
            # these directories are generated with the
            # create_organisations_upload_directories command
            zipfiles = [os.path.join(dirpath, f)
                        for dirpath, dirnames, files
                        in os.walk(ftp_upload_path)
                        for f in files if f.endswith('.zip')]
            # apply last modified time filter; only process zipfiles that are
            # not changed for at least 60 seconds
            zipfiles = [zipfile for zipfile in zipfiles
                        if time.time() > os.path.getmtime(zipfile) + 60]
            if not zipfiles:
                sys.stdout.write("No zipfiles found for processing.\n")
            # filter on last modified date
            for zipfile in zipfiles:
                fpath, fn = os.path.split(zipfile)
                org_name = os.path.split(fpath)[1]
                try:
                    organisation = Organisation.objects.get(name=org_name)
                except ObjectDoesNotExist:
                    sys.stdout.write("No organisation found with name %s.\n" %
                                     org_name)
                    continue
                else:
                    sys.stdout.write(
                        "Processing zipfile %s for organisation %s...\n" % (
                            fn, organisation))
                    fn_wo_zip = fn.rstrip('.zip').capitalize()

                    # check for duplicate model name
                    try:
                        ModelReference.objects.get(identifier=fn_wo_zip)
                    except ObjectDoesNotExist:
                        pass
                    else:
                        sys.stdout.write(
                            "Model with name %s already exists. Removing "
                            "uploaded zipfile %s." % (fn_wo_zip, fn))
                        os.remove(zipfile)
                        continue

                    ftp_user = get_ftp_user()
                    now = datetime.datetime.now()
                    file_name = '%s_%s.zip' % (
                        fn_wo_zip, now.strftime('%Y%m%d%H%M%S%f'))
                    file_path = os.path.join(
                        settings.MODEL_DATABANK_UPLOAD_PATH, file_name)
                    # For now, assume a model uploaded by FTP is a 3Di model;
                    # this can be changed via the ModelReference admin page.
                    default_model_type = ModelType.objects.get(slug='3di')
                    try:
                        shutil.move(zipfile, file_path)
                        model_upload = ModelUpload(
                            uploaded_by=ftp_user, identifier=fn_wo_zip,
                            description='', file_path=file_path,
                            organisation=organisation,
                            model_type=default_model_type)
                        model_upload.save()
                    except Exception, err:
                        sys.stdout.write(
                            "An error occurred trying to prepare a "
                            "ModelUpload instance. Error: %s.\n" % err)

        # make mercurial repositories of the unprocessed ModelUpload instances
        unprocessed_model_uploads = ModelUpload.objects.filter(
            is_processed=False)

        if not unprocessed_model_uploads:
            sys.stdout.write("No model uploads to process.\n")

        for model_upload in unprocessed_model_uploads:
            model_upload.process()
            sys.stdout.write("Made mercurial repository for %s.\n" %
                             model_upload)

        # cleanup uploaded zip files that are older than 14 days
        delete_after = datetime.datetime.now() - datetime.timedelta(days=14)
        old_model_uploads = ModelUpload.objects.filter(
            ~Q(file_path=''), uploaded__lte=delete_after)
        if not old_model_uploads:
            sys.stdout.write("No model upload zipfiles found for removal "
                             "(older than 14 days).\n")
        for old_model_upload in old_model_uploads:
            make_file_path_empty = False
            try:
                os.remove(old_model_upload.file_path)
                make_file_path_empty = True
            except OSError, err:
                if 'no such file' in str(err).lower():
                    # zipfile probably removed by hand already, so set file
                    # path to '' anyway
                    make_file_path_empty = True
                else:
                    sys.stdout.write(
                        "Removing old model upload zipfile %s failed. Error: "
                        "%s.\n" % (old_model_upload.file_path, err))
            if make_file_path_empty:
                old_model_upload.file_path = ''
                old_model_upload.save()
                sys.stdout.write("Made file_path emtpy for %s.\n"
                                 % old_model_upload)
