# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from model_databank import models


class ModelReferenceAdmin(admin.ModelAdmin):

    readonly_fields = ('uuid',)
    list_display = ('identifier', 'model_type', 'uuid', 'created')


def process_upload(modeladmin, request, queryset):
    queryset.update(status='p')
process_upload.short_description = "Process selected model upload files."


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
