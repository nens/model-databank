# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import datetime
from django.contrib import messages
import os

from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
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

from django.views.generic import FormView, ListView, DetailView

from model_databank.conf import settings
from model_databank.forms import NewModelUploadForm
from model_databank.models import ModelUpload, ModelReference
from model_databank.utils import zip_model_files
from model_databank.vcs_utils import get_log, get_file_tree


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


class ModelDownloadView(DetailView):
    """Download zip file from tip of repo."""
    model = ModelReference

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        zip_file_path, revision = zip_model_files(self.object)
        zip_file = open(zip_file_path, 'rb')
        response = HttpResponse(FileWrapper(zip_file),
                                content_type='application/zip')
        file_name = '%s-%s.zip' % (self.object.slug, revision)
        response['Content-Disposition'] = 'attachment; filename=%s' % file_name
        return response


class ModelReferenceList(ListView):
    model = ModelReference


class ModelReferenceDetail(DetailView):
    model = ModelReference

    def get_context_data(self, object, **kwargs):
        context = super(ModelReferenceDetail, self).get_context_data(
            object=object, **kwargs)
        log_data = get_log(object)
        context['log_data'] = log_data
        return context


class CommitView(DetailView):
    """Show commit specific details."""
    model = ModelReference
    template_name = 'model_databank/commit_detail.html'

    def get_context_data(self, object, **kwargs):
        context = super(CommitView, self).get_context_data(
            object=object, **kwargs)
        revision = self.kwargs.get('revision')
        log_data = get_log(object, revision)
        context['log_data'] = log_data
        return context


class FilesView(DetailView):
    """Show files belonging to the ModelReference instance."""
    model = ModelReference
    template_name = 'model_databank/files.html'

    def get_context_data(self, object, **kwargs):
        context = super(FilesView, self).get_context_data(
            object=object, **kwargs)
        file_tree = get_file_tree(object)
        context['file_tree'] = file_tree
        return context
