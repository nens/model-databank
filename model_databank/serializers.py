from model_databank.models import ModelReference

from rest_framework import serializers


class ModelReferenceSerializer(serializers.ModelSerializer):

    repository_url = serializers.Field()

    class Meta:
        model = ModelReference
        fields = ('identifier', 'repository_url')
