from django.conf import settings
from appconf import AppConf


class ModelDatabankAppConf(AppConf):
    """App specific settings. Overridable in global settings.

    DATA_PATH: path to the real mercurial repositories; these should never
        be manipulated directly. Active repositories are symlinked in the
        SYMLINK_PATH directory by their slug name.

    SYMLINK_PATH: path with symlinks to active model reference repositories.

    UPLOAD_PATH: uploaded zip files end up in this directory.

    ZIP_EXTRACT_PATH: the uploaded zip files are extracted in this directory.

    DOWNLOAD_PATH: repositories that are zipped for download are put in here.

    REPOSITORY_URL_ROOT: root url for cloning repositories.

    MAX_REVISIONS: maximum total number of revisions shown for a model

    MAX_REVISIONS_PER_PAGE: maximum number of revisions per page.
    """
    DATA_PATH = "/tmp/model_databank_repositories"
    SYMLINK_PATH = "/tmp/model_databank"
    UPLOAD_PATH = "/tmp/uploads"
    ZIP_EXTRACT_PATH = "/tmp/extracted_zip_files/"
    DOWNLOAD_PATH = "/tmp/downloads"
    REPOSITORY_URL_ROOT = 'http://127.0.0.1:8012'
    MAX_REVISIONS = 500
    MAX_REVISIONS_PER_PAGE = 100

    class Meta:
        prefix = 'model_databank'
