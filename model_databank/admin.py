# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import os
import logging
import shutil

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from model_databank import models

logger = logging.getLogger(__name__)


class ModelReferenceAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'model_type', 'slug', 'uuid', 'is_deleted',
                    'created')
    readonly_fields = ('uuid', 'slug')

    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        # TODO: add try block and return message if something fails
        for model_reference in queryset:
            # remove symlink
            if os.path.exists(model_reference.symlink):
                os.unlink(model_reference.symlink)
            # remove repository
            shutil.rmtree(model_reference.repository)
            model_reference.delete()
    delete_selected.short_description = _("Delete selected models permanently")


class ModelUploadAdmin(admin.ModelAdmin):

    list_display = ('model_reference', 'identifier', 'description',
                    'file_path', 'is_processed', 'uploaded')

    actions = ['make_processed']

    def make_processed(self, request, queryset):
        processed_count = 0
        for obj in queryset:
            try:
                processed_obj = obj.process()
            except:
                logger.exception("Caught unexpected exception.")
            else:
                if processed_obj:  # could be None in case something went wrong
                    processed_count += 1
                else:
                    logger.error("Could not process %s." % obj)
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
