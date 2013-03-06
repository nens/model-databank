# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.contrib import admin

from model_databank import models


class ModelReferenceAdmin(admin.ModelAdmin):

    readonly_fields = ('uuid',)
    list_display = ('identifier', 'model_type', 'uuid', 'created')


class ModelUploadAdmin(admin.ModelAdmin):

    list_display = ('model_reference', 'identifier', 'description',
                    'file_path', 'is_processed', 'uploaded')


admin.site.register(models.ModelReference, ModelReferenceAdmin)
admin.site.register(models.ModelUpload, ModelUploadAdmin)
