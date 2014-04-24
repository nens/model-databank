from model_databank.models import ModelReference

from rest_framework import serializers


class ModelReferenceSerializer(serializers.ModelSerializer):

    repository_url = serializers.Field()
    organisation_uuid = serializers.Field()
    repository_ssh_url = serializers.Field()

    class Meta:
        model = ModelReference
        fields = ('identifier', 'repository_url', 'organisation_uuid',
                  'repository_ssh_url', 'slug')
