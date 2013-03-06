import os
import sys
import shutil
import zipfile

from django.core.management.base import BaseCommand
from model_databank.models import ModelUpload, ModelReference
from model_databank.conf import settings


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


class Command(BaseCommand):
    help = 'Processes the uploaded unprocessed model zip files.'

    def handle(self, *args, **options):
        unprocessed_model_uploads = ModelUpload.objects.filter(
            is_processed=False)

        if not unprocessed_model_uploads:
            sys.stdout.write("No model uploads to process.\n")
            sys.exit(1)

        for model_upload in unprocessed_model_uploads:
            # (check if this is a zip file, later)
            # unzip zip file in tmp directory
            try:
                z = zipfile.ZipFile(model_upload.file_path)
            except zipfile.BadZipfile:
                sys.stdout.write("File is not a zip file: %s\n" %
                                 model_upload.file_path)
                continue
            except IOError, msg:
                sys.stdout.write("%s\n" % msg)
                continue
            extract_to = os.path.join(
                settings.MODEL_DATABANK_ZIP_EXTRACT_PATH, str(model_upload.id))
            z.extractall(path=extract_to)

            # create repo dir if not exist
            if not model_upload.model_reference:
                # convert to hg repo
                os.chdir(extract_to)
                os.system('/usr/local/bin/hg init')
                # loop through files and add files from largefiles extensions
                # to
                largefiles_file_paths = get_largefiles_file_paths(extract_to)
                for fp in largefiles_file_paths:
                    # this is needed even when a largefiles patterns entry
                    # is added to ~/.hgrc
                    os.system('/usr/local/bin/hg add --large %s' % fp)
                    sys.stdout.write("Added %s as large file to repository\n"
                                     % fp)

                os.system('/usr/local/bin/hg add')
                os.system('/usr/local/bin/hg commit -m "Initial commit."')

                # if we got here, create a ModelReference with uuid for the
                # repo dir naming

                model_reference = ModelReference(
                    model_type=ModelReference.THREEDI_MODEL_TYPE_ID,
                    identifier=model_upload.identifier,
                    comment=model_upload.description)
                model_reference.save()

                repo_dir = os.path.join(settings.MODEL_DATABANK_DATA_PATH,
                                        str(model_reference.uuid))
                shutil.move(extract_to, repo_dir)

                model_upload.model_reference = model_reference
                model_upload.is_processed = True
                model_upload.save()
