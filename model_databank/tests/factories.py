import factory

from model_databank import models


class ModelReferenceFactory(factory.Factory):
    """ModelReference factory.

    Can generate many ModelReference instances in a for loop, for example.

    """
    FACTORY_FOR = models.ModelReference

    identifier = factory.Sequence(lambda n: 'model {0}'.format(n))


class VersionFactory(factory.Factory):
    FACTORY_FOR = models.Version

    name = factory.Sequence(lambda n: 'version {0}'.format(n))


class VariantFactory(factory.Factory):
    FACTORY_FOR = models.Variant

    name = factory.Sequence(lambda n: 'variant {0}'.format(n))
