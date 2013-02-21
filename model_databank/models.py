# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.db import models
from django.utils.translation import ugettext_lazy as _

from autoslug import AutoSlugField


class ModelReference(models.Model):
    """
    Work in progress. Mainly sketching to get a feel with the whole matter.

    Considerations
    --------------
    - Model naming: naming this class 'Model' is a no go, since the confusion 
      it might give with django.db.models.Model.
    - Since it is mainly a reference to either a path or some metadata, we now
      chose to name it ModelReference. Other more or less viable ideas were
      ModelData, ModelInfo, ModelWrapper.
    
    - Metadata:

      In flooding relevant information about the different models is stored in
      the model itself; e.g. the SobekModel class has lots of fields that
      defines a Sobek model. A ThreediModel is merely a pointer to the mdu
      filename and to the scenario zip file name.
      
      To make this more flexible one idea is to make this class very compact
      and to add metadata about it in a document-based database, for example 
      something like MongoDB.
      
      In order to make this work we somehow need a way to add and edit this
      (MongoDB) metadata document through some kind of admin page wrapping 
      that document.

    """
    MODEL_TYPE_CHOICES = (
        (1, 'Sobek'),
        (2, '3Di'),
    )
    
    model_type = models.IntegerField(
        verbose_name=_("model type"), choices=MODEL_TYPE_CHOICES)
    
    # Unique identifier for this model, not sure whether this is the way to go, 
    # but in order to store metadata in MongoDB without a non-descriptive id
    # (pk) it could be desirable to have a more descriptive identifier with
    # automatically generated slug.  
    identifier = models.CharField(
        verbose_name=_("unique identifier"), max_length=200, unique=True)
    slug = AutoSlugField(populate_from='identifier')

    def __unicode__(self):
        model_type = dict(self.MODEL_TYPE_CHOICES)[self.model_type]
        return _("%(identifier)s (%(type)s model)") % {
            'identifier': self.identifier, 'type': model_type}

