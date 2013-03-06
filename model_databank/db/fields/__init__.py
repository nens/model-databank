"""
UUIDField from Django Extensions additional model fields

See django_extensions/db/fields/__init__.py

"""
import six

import uuid
assert uuid

from django.db.models import CharField

try:
    from django.utils.timezone import now as datetime_now
    assert datetime_now
except ImportError:
    import datetime
    datetime_now = datetime.datetime.now

try:
    from django.utils.encoding import force_unicode
except ImportError:
    from django.utils.encoding import force_text as force_unicode


class UUIDVersionError(Exception):
    pass


class UUIDField(CharField):
    """ UUIDField

    By default uses UUID version 4 (generate from host ID, sequence number and
    current time)

    The field support all uuid versions which are natively supported by the
    uuid python module.
    For more information see: http://docs.python.org/lib/module-uuid.html
    """

    def __init__(self, verbose_name=None, name=None, auto=True, version=1,
                 node=None, clock_seq=None, namespace=None, **kwargs):
        kwargs.setdefault('max_length', 36)
        if auto:
            self.empty_strings_allowed = False
            kwargs['blank'] = True
            kwargs.setdefault('editable', False)
        self.auto = auto
        self.version = version
        if version == 1:
            self.node, self.clock_seq = node, clock_seq
        elif version == 3 or version == 5:
            self.namespace, self.name = namespace, name
        CharField.__init__(self, verbose_name, name, **kwargs)

    def get_internal_type(self):
        return CharField.__name__

    def contribute_to_class(self, cls, name):
        if self.primary_key:
            assert not cls._meta.has_auto_field, (
                "A model can't have more than one AutoField: %s %s %s; have "
                "%s") % (self, cls, name, cls._meta.auto_field)
            super(UUIDField, self).contribute_to_class(cls, name)
            cls._meta.has_auto_field = True
            cls._meta.auto_field = self
        else:
            super(UUIDField, self).contribute_to_class(cls, name)

    def create_uuid(self):
        if not self.version or self.version == 4:
            return uuid.uuid4()
        elif self.version == 1:
            return uuid.uuid1(self.node, self.clock_seq)
        elif self.version == 2:
            raise UUIDVersionError("UUID version 2 is not supported.")
        elif self.version == 3:
            return uuid.uuid3(self.namespace, self.name)
        elif self.version == 5:
            return uuid.uuid5(self.namespace, self.name)
        else:
            raise UUIDVersionError("UUID version %s is not valid." %
                                   self.version)

    def pre_save(self, model_instance, add):
        value = super(UUIDField, self).pre_save(model_instance, add)
        if self.auto and add and value is None:
            value = force_unicode(self.create_uuid())
            setattr(model_instance, self.attname, value)
            return value
        else:
            if self.auto and not value:
                value = six.u(self.create_uuid())
                setattr(model_instance, self.attname, value)
        return value

    def formfield(self, **kwargs):
        if self.auto:
            return None
        return super(UUIDField, self).formfield(**kwargs)

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect the _actual_ field.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        # That's our definition!
        return (field_class, args, kwargs)
