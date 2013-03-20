import sys

from django.core.management.base import BaseCommand
from model_databank.models import ModelUpload


class Command(BaseCommand):
    help = 'Process the uploaded unprocessed model zip files.'

    def handle(self, *args, **options):
        unprocessed_model_uploads = ModelUpload.objects.filter(
            is_processed=False)

        if not unprocessed_model_uploads:
            sys.stdout.write("No model uploads to process.\n")

        for model_upload in unprocessed_model_uploads:
            # (check if this is a zip file, later)
            model_upload.process()
