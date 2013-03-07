from django.conf import settings
from appconf import AppConf


class ModelDatabankAppConf(AppConf):
    """App specific settings. Overridable in global settings."""
    DATA_PATH = "/tmp/model_databank"  # path to model, version, and variant files
    UPLOAD_PATH = "/tmp/uploads"
    ZIP_EXTRACT_PATH = "/tmp/extracted_zip_files/"
    DOWNLOAD_PATH = "/tmp/downloads"

    class Meta:
        prefix = 'model_databank'
