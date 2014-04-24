import os
import sys

from django.conf import settings
from django.core.management.base import BaseCommand

from lizard_auth_client.models import Organisation


class Command(BaseCommand):
    help = 'Update `last_repo_update` of ModelReference instances.'

    def handle(self, *args, **options):
        # Check latest commit/update of the repo and if it differs from
        # the existing last_repo_update, save the new update date.
        organisations = Organisation.objects.all()
        for organisation in organisations:
            ftp_upload_path = os.path.join(
                settings.MODEL_DATABANK_FTP_UPLOAD_PATH, organisation.name)
            if not os.path.exists(ftp_upload_path):
                os.makedirs(ftp_upload_path)
                sys.stdout.write("Created ftp upload directory %s.\n" %
                                 ftp_upload_path)
