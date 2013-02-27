from django.conf import settings
from appconf import AppConf


class ModelDatabankAppConf(AppConf):
    """App specific settings. Overridable in global settings."""
    DATA_PATH = "/tmp"  # path to model, version, and variant files

    class Meta:
        prefix = 'model_databank'
