import os
import errno
import logging

from django.core.management.base import BaseCommand

from django.conf import settings


logger = logging.getLogger(__name__)


def symlink_force(link_name, target):
    try:
        logger.info('target %s, link_name %s ', target, link_name)
        os.symlink(target, link_name)
    except OSError as e:
        logger.warning(e)
        if e.errno == errno.EEXIST:
            os.remove(link_name)
            os.symlink(target, link_name)
            logger.info("Renamed %s to %s ", target, link_name)


class Command(BaseCommand):

    def handle(self, *args, **options):

        names = os.listdir(settings.MODEL_DATABANK_SYMLINK_PATH)
        for name in names:
            target = os.path.join(settings.MODEL_DATABANK_SYMLINK_PATH, name)
            repo_uuid = os.path.basename(os.readlink(target))
            link_name = os.path.join(
                settings.MODEL_DATABANK_DATA_PATH, repo_uuid
            )
            symlink_force(target, link_name)
