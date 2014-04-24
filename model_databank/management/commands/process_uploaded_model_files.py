from lizard_auth_client.models import Organisation
import os
import sys
import datetime
import random
import shutil
import string

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from model_databank.models import ModelUpload


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
                    ftp_user = get_ftp_user()
                    now = datetime.datetime.now()
                    file_name = '%s.zip' % now.strftime('%Y%m%d%H%M%S')
                    file_path = os.path.join(
                        settings.MODEL_DATABANK_UPLOAD_PATH, file_name)
                    try:
                        shutil.move(zipfile, file_path)
                        model_upload = ModelUpload(
                            uploaded_by=ftp_user, identifier=fn_wo_zip,
                            description='TODO', file_path=file_path,
                            organisation=organisation)
                        model_upload.save()
                    except Exception, err:
                        sys.stdout.write(
                            "An error occurred trying to prepare a "
                            "ModelUpload instance. Error: %s.\n" % err)

        # now, process the unprocessed ModelUpload instances
        unprocessed_model_uploads = ModelUpload.objects.filter(
            is_processed=False)

        if not unprocessed_model_uploads:
            sys.stdout.write("No model uploads to process.\n")

        for model_upload in unprocessed_model_uploads:
            # (check if this is a zip file, later)
            model_upload.process()
