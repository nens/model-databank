import factory

from model_databank import models


class ModelReferenceFactory(factory.django.DjangoModelFactory):
    """ModelReference factory.

    Can generate many ModelReference instances in a for loop, for example.

    """
    class Meta:
        model = models.ModelReference

    identifier = factory.Sequence(lambda n: 'model {0}'.format(n))
    slug = factory.Sequence(lambda n: 'slug_{0}'.format(n))


class VersionFactory(factory.Factory):
    class Meta:
        model = models.Version

    name = factory.Sequence(lambda n: 'version {0}'.format(n))


class VariantFactory(factory.Factory):
    class Meta:
        model = models.Variant

    name = factory.Sequence(lambda n: 'variant {0}'.format(n))
