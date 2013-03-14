# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import os
import shutil

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from model_databank import models


class ModelReferenceAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'model_type', 'slug', 'uuid', 'created')
    readonly_fields = ('uuid', 'slug')

    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        for model_reference in queryset:
            # remove symlink
            if os.path.exists(model_reference.symlink):
                os.unlink(model_reference.symlink)
            # remove repository
            shutil.rmtree(model_reference.repository)
            # remove object
            model_reference.delete()
    delete_selected.short_description = _("Delete selected model uploads")


class ModelUploadAdmin(admin.ModelAdmin):

    list_display = ('model_reference', 'identifier', 'description',
                    'file_path', 'is_processed', 'uploaded')

    actions = ['make_processed']

    def make_processed(self, request, queryset):
        processed_count = 0
        for obj in queryset:
            processed_obj = obj.process()
            if processed_obj:
                processed_count += 1
        if processed_count:
            if processed_count == 1:
                message_bit = _("1 model upload was")
            else:
                message_bit = _("%s model uploads were") % processed_count
            self.message_user(request, _("%s successfully processed.") %
                              message_bit)
        else:
            self.message_user(request, _("No model uploads were processed."))
    make_processed.short_description = _("Process selected model uploads")


admin.site.register(models.ModelReference, ModelReferenceAdmin)
admin.site.register(models.ModelUpload, ModelUploadAdmin)
