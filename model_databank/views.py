# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import datetime
import os

from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView

from wsgiref.util import FileWrapper

from lizard_auth_client.models import Organisation

from rest_framework.response import Response
from rest_framework.views import APIView

from model_databank.conf import settings
from model_databank.forms import ModelUploadForm
from model_databank.mixins import RoleRequiredRemoteMixin
from model_databank.models import ModelReference
from model_databank.models import ModelType
from model_databank.models import ModelUpload
from model_databank.serializers import ModelReferenceSerializer
from model_databank.utils import get_organisation_ids_by_user_permission
from model_databank.utils import zip_model_files
from model_databank.vcs_utils import get_file_tree
from model_databank.vcs_utils import get_log


def handle_uploaded_file(f):
    now = datetime.datetime.now()
    file_name = '%s.zip' % now.strftime('%Y%m%d%H%M%S')
    file_path = os.path.join(settings.MODEL_DATABANK_UPLOAD_PATH, file_name)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path


class ModelUploadFormView(
        RoleRequiredRemoteMixin, FormView):
    """Form view for uploading model files."""
    permission_denied_message = _(
        "You don't have enough permissions to access this page.\n"
        "Please contact your administrator to get permission."
    )
    role_required = 'change_model'
    template_name = 'model_databank/upload_form.html'
    form_class = ModelUploadForm

    def get_success_url(self):
        return reverse('model_reference_list')

    def get_form_kwargs(self):
        kwargs = super(ModelUploadFormView, self).get_form_kwargs()
        # add request to get the organisation the request.user belongs to in
        # the form
        kwargs.update(request=self.request)
        return kwargs

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # handle file upload
        # write file in chunks to file system
        file_path = handle_uploaded_file(self.request.FILES['upload_file'])
        identifier = form.cleaned_data.get('model_name')
        description = form.cleaned_data.get('description')
        organisation_uuid = form.cleaned_data.get('organisation')
        organisation = Organisation.objects.get(unique_id=organisation_uuid)
        model_type_id = form.cleaned_data.get('model_type')
        model_type = ModelType.objects.get(pk=model_type_id)
        model_upload = ModelUpload(
            uploaded_by=self.request.user, identifier=identifier,
            description=description, file_path=file_path,
            organisation=organisation, model_type=model_type)
        model_upload.save()
        messages.info(self.request, _("Upload succeeded. Data will be "
                                      "processed soon."))
        return super(ModelUploadFormView, self).form_valid(form)

    # N.B. the methods below this point are needed because the
    # RoleRequiredRemoteMixin overrides the dispatch() method
    def handle_not_logged_in(self):
        return redirect_to_login(
            self.request.get_full_path(), settings.LOGIN_URL,
            REDIRECT_FIELD_NAME)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_not_logged_in()
        return super(ModelUploadFormView, self).dispatch(
            request, *args, **kwargs)


class ModelDownloadView(LoginRequiredMixin, DetailView):
    """Download zip file from tip of repo."""
    queryset = ModelReference.active.all()

    def get_queryset(self):
        queryset = super(ModelDownloadView, self).get_queryset()
        # organisation ids belonging to the change_model permission
        organisation_ids = get_organisation_ids_by_user_permission(
            self.request.user, 'change_model')
        return queryset.filter(
            organisation__unique_id__in=organisation_ids)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        zip_file_path, revision = zip_model_files(self.object)
        zip_file = open(zip_file_path, 'rb')
        response = HttpResponse(FileWrapper(zip_file),
                                content_type='application/zip')
        file_name = '%s-%s.zip' % (self.object.slug, revision)
        response['Content-Disposition'] = 'attachment; filename=%s' % file_name
        return response


class ModelReferenceList(LoginRequiredMixin, ListView):
    """
    List view showing ModelReference instances.

    Get the user organisation ids and only show the ModelReference instances
    for those organisations.

    """
    queryset = ModelReference.active.all()

    def get_queryset(self):
        queryset = super(ModelReferenceList, self).get_queryset()
        # organisation ids belonging to the change_model permission
        organisation_ids = get_organisation_ids_by_user_permission(
            self.request.user, 'change_model')
        return queryset.filter(
            organisation__unique_id__in=organisation_ids)


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


class ModelReferenceBaseView(LoginRequiredMixin, NavbarMixin, DetailView):
    """
    Base view for ModelReference detail views.

    Uses the organisation ids from the RoleRequiredRemoteMixin to filter the
    queryset, that is used by the get_object method.

    """
    def get_queryset(self):
        queryset = ModelReference.active.all()
        organisation_ids = get_organisation_ids_by_user_permission(
            self.request.user, 'change_model')
        return queryset.filter(organisation__unique_id__in=organisation_ids)


class ModelReferenceDetail(ModelReferenceBaseView):
    """ModelReference detail view."""
    def get_context_data(self, **kwargs):
        context = super(ModelReferenceDetail, self).get_context_data(**kwargs)
        obj = self.get_object()
        log_data = get_log(obj,
                           limit=settings.MODEL_DATABANK_MAX_REVISIONS).log_data
        page = self.request.GET.get('page', 1)
        paginator = Paginator(log_data,
                              settings.MODEL_DATABANK_MAX_REVISIONS_PER_PAGE)
        log_data_page = paginator.page(page)
        context['log_data_page'] = log_data_page
        return context


class FilesView(ModelReferenceBaseView):
    """Show files belonging to the ModelReference instance."""
    template_name = 'model_databank/files.html'

    def get_context_data(self, **kwargs):
        context = super(FilesView, self).get_context_data(**kwargs)
        obj = self.get_object()
        file_tree = get_file_tree(obj)
        page = self.request.GET.get('page', 1)
        paginator = Paginator(file_tree, 100)
        file_tree_page = paginator.page(page)
        context['file_tree_page'] = file_tree_page
        return context


class CommitView(LoginRequiredMixin, DetailView):
    """Show commit specific details."""
    queryset = ModelReference.active.all()
    template_name = 'model_databank/commit_detail.html'

    def get_queryset(self):
        queryset = super(CommitView, self).get_queryset()
        # organisation ids belonging to the change_model permission
        organisation_ids = get_organisation_ids_by_user_permission(
            self.request.user, 'change_model')
        return queryset.filter(
            organisation__unique_id__in=organisation_ids)

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

    N.B.: no restrictions on this view -> open for everybody! Is used by inpy
    (get_model_repositories).

    """
    def get(self, request, format=None):
        model_references = ModelReference.active.all()
        serializer = ModelReferenceSerializer(model_references, many=True)
        return Response(serializer.data)
