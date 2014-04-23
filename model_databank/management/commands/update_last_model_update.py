import sys

from django.core.management.base import BaseCommand

from model_databank.models import ModelReference
from model_databank.vcs_utils import get_last_update_date


class Command(BaseCommand):
    help = 'Update `last_repo_update` of ModelReference instances.'

    def handle(self, *args, **options):
        # Check latest commit/update of the repo and if it differs from
        # the existing last_repo_update, save the new update date.
        model_refs = ModelReference.objects.all()
        for model_ref in model_refs:
            last_update = get_last_update_date(model_ref)
            if not last_update == model_ref.last_repo_update:
                model_ref.last_repo_update = last_update
                model_ref.save()
                sys.stdout.write("Updated last_repo_date field of model "
                                 "reference %s.\n" % model_ref)
