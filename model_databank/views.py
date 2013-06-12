# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import datetime
from django.contrib import messages
import os
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
# from django.core.urlresolvers import reverse
# from lizard_map.views import MapView
# from lizard_ui.views import UiView

# from model_databank import models

from django.views.generic import FormView, ListView, DetailView

from braces.views import LoginRequiredMixin

from model_databank.conf import settings
from model_databank.forms import NewModelUploadForm
from model_databank.models import ModelUpload, ModelReference
from model_databank.serializers import ModelReferenceSerializer
from model_databank.utils import zip_model_files
from model_databank.vcs_utils import get_log, get_file_tree

from rest_framework.response import Response
from rest_framework.views import APIView


def handle_uploaded_file(f):
    now = datetime.datetime.now()
    file_name = '%s.zip' % now.strftime('%Y%m%d%H%M%S')
    file_path = os.path.join(settings.MODEL_DATABANK_UPLOAD_PATH, file_name)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path


class NewModelUploadFormView(LoginRequiredMixin, FormView):
    """Form view for uploading model files."""
    template_name = 'model_databank/upload_form.html'
    form_class = NewModelUploadForm

    def get_success_url(self):
        return reverse('model_reference_list')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # handle file upload
        # write file in chunks to file system
        file_path = handle_uploaded_file(self.request.FILES['upload_file'])
        identifier = form.cleaned_data.get('model_name')
        description = form.cleaned_data.get('description')
        model_upload = ModelUpload(
            uploaded_by=self.request.user, identifier=identifier,
            description=description, file_path=file_path)
        model_upload.save()
        messages.info(self.request, _("Upload succeeded. Data will be "
                                      "processed soon."))
        return super(NewModelUploadFormView, self).form_valid(form)


class ModelDownloadView(DetailView):
    """Download zip file from tip of repo."""
    queryset = ModelReference.active.all()

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
    queryset = ModelReference.active.all()


class NavbarMixin(object):
    """Navigation links for model reference views.

    Does not include the url if the current url equals the reversed url.
    This can be used to display the active navigation link in the template.

    """
    navbar_items = (
        (_('Commits'), 'model_reference_detail'),
        (_('Files'), 'model_reference_files'),
    )

    def get_context_data(self, **kwargs):
        context = super(NavbarMixin, self).get_context_data(**kwargs)
        obj = self.get_object()
        current_url = self.request.path
        navbar_entries = []
        for url_name, url_id in self.navbar_items:
            navbar_entry = {'name': url_name}
            url = reverse(url_id, kwargs={'slug': obj.slug})
            if not url == current_url:
                navbar_entry['url'] = url
            navbar_entries.append(navbar_entry)
        context['section_navbar_items'] = navbar_entries
        return context


class ModelReferenceBaseView(NavbarMixin, DetailView):
    queryset = ModelReference.active.all()


class ModelReferenceDetail(ModelReferenceBaseView):

    def get_context_data(self, **kwargs):
        context = super(ModelReferenceDetail, self).get_context_data(**kwargs)
        obj = self.get_object()
        log_data = get_log(obj)
        context['log_data'] = log_data
        return context


class FilesView(ModelReferenceBaseView):
    """Show files belonging to the ModelReference instance."""
    template_name = 'model_databank/files.html'

    def get_context_data(self, **kwargs):
        context = super(FilesView, self).get_context_data(**kwargs)
        obj = self.get_object()
        file_tree = get_file_tree(obj)
        context['file_tree'] = file_tree
        return context


class CommitView(DetailView):
    """Show commit specific details."""
    queryset = ModelReference.active.all()
    template_name = 'model_databank/commit_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CommitView, self).get_context_data(**kwargs)
        revision = self.kwargs.get('revision')
        obj = self.get_object()
        log_data = get_log(obj, revision)
        context['log_data'] = log_data
        return context


# rest framework views
class ApiModelReferenceList(APIView):
    """
    API view for handling active model references snippets.

    """
    def get(self, request, format=None):
        model_references = ModelReference.active.all()
        serializer = ModelReferenceSerializer(model_references)
        return Response(serializer.data)
