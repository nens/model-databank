# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import datetime
from django.contrib import messages
import os

from django.utils.translation import ugettext as _
# from django.core.urlresolvers import reverse
# from lizard_map.views import MapView
# from lizard_ui.views import UiView

# from model_databank import models


# class TodoView(UiView):
#     """Simple view without a map."""
#     template_name = 'model_databank/todo.html'
#     page_title = _('TODO view')


# class Todo2View(MapView):
#     """Simple view with a map."""
#     template_name = 'model_databank/todo2.html'
#     page_title = _('TODO 2 view')

from django.views.generic import FormView

from model_databank.conf import settings
from model_databank.forms import NewModelUploadForm
from model_databank.models import ModelUpload


def handle_uploaded_file(f):
    now = datetime.datetime.now()
    file_name = '%s.zip' % now.strftime('%Y%m%d%H%M%S')
    file_path = os.path.join(settings.MODEL_DATABANK_UPLOAD_PATH, file_name)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path


class NewModelUploadFormView(FormView):
    """Form view for uploading model files."""
    template_name = 'model_databank/upload_form.html'
    form_class = NewModelUploadForm
    success_url = '/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # handle file upload
        # write file in chunks to file system
        file_path = handle_uploaded_file(self.request.FILES['upload_file'])
        identifier = form.cleaned_data.get('model_name')
        description = form.cleaned_data.get('description')
        model_upload = ModelUpload(
            identifier=identifier, description=description,
            file_path=file_path)
        model_upload.save()
        messages.info(self.request, _("Upload succeeded. Data will be "
                                      "processed soon."))
        return super(NewModelUploadFormView, self).form_valid(form)
