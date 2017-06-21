# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
import os
import subprocess
import zipfile

import requests

from model_databank.conf import settings
from model_databank.vcs_utils import get_latest_revision


def zip_dir(path, zip_file):
    for root, dirs, files in os.walk(path):
        if '.hg' in root:
            continue
        for _file in files:
            filename = os.path.join(root, _file)
            arcname = os.path.join(root.lstrip(path), _file)
            zip_file.write(filename, arcname, zipfile.ZIP_DEFLATED)


def zip_model_files(model_reference):
    repo_path = model_reference.symlink
    os.chdir(repo_path)
    subprocess.call([settings.HG_CMD, 'up'])  # update to tip
    latest_revision = get_latest_revision(model_reference)
    file_name = '%s-%s.zip' % (model_reference.uuid, latest_revision)
    zip_file_full_path = os.path.join(settings.MODEL_DATABANK_DOWNLOAD_PATH,
                                      file_name)
    zip_file = zipfile.ZipFile(zip_file_full_path, 'w')
    zip_dir(repo_path, zip_file)
    zip_file.close()
    return zip_file_full_path, latest_revision


def get_organisation_ids_by_user_permission(user, permission):
    """
    Return the organisation ids the user has the permission for.

    :raise - requests.exceptions.HttpError when status code is not ok (2xx)
    :return - list of organisation ids

    """
    permissions_api_url = '{}{}/{}/'.format(
        settings.PERMISSIONS_API_URL, user.username, permission)
    # get the organisation ids for the username / role combo
    resp = requests.get(permissions_api_url)
    resp.raise_for_status()
    return resp.json()
