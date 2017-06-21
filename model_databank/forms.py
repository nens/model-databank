# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
import logging

from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset
from crispy_forms.layout import Layout
from crispy_forms.layout import Submit

from lizard_auth_client.models import Organisation

from model_databank.models import ModelType
from model_databank.utils import get_organisation_ids_by_user_permission

logger = logging.getLogger(__name__)


def get_organisation_choices(user):
    """Create organisation choices for model upload form."""
    allowed_organisation_ids = get_organisation_ids_by_user_permission(
        user, 'change_model')
    organisations = Organisation.objects.filter(
        unique_id__in=allowed_organisation_ids)
    organisation_choices = []
    for organisation in organisations:
        organisation_choices.append((organisation.unique_id,
                                     organisation.name))
    return tuple(organisation_choices)


def get_model_type_choices():
    """Model type choices for model upload form. Default is 3Di because it is
    the first."""
    model_types = ModelType.objects.all()
    model_type_choices = []
    for model_type in model_types:
        model_type_choices.append((model_type.pk, model_type.name))
    return tuple(model_type_choices)


class ModelUploadForm(forms.Form):
    """Model for uploading new zipped model files."""
    upload_file = forms.FileField(
        required=True, label=_("Upload ZIP file"),
        help_text=_("Provide your model files by compressing them into "
                    "a zip file."))
    model_name = forms.CharField(
        label=_("Model name"), max_length=200,
        help_text=_("Concise and descriptive name for this model."))
    description = forms.CharField(
        label=_("Description"),
        widget=forms.Textarea,
        help_text=_("Describe as accurately as possible what this model "
                    "does."))
    organisation = forms.ChoiceField(
        label=_("Organisation"),
        widget=forms.Select,
        choices=[],
        help_text=_("Pick the organisation this model belongs too."))
    model_type = forms.ChoiceField(
        label=_("Model type"),
        widget=forms.Select,
        choices=[],
        help_text=_("Choose model type."))

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        if request:
            # set organisation choices
            organisation_choices = get_organisation_choices(
                request.user)
            self.base_fields['organisation'].choices = organisation_choices
            # set model type choices
            model_type_choices = get_model_type_choices()
            self.base_fields['model_type'].choices = model_type_choices

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.html5_required = True
        self.helper.layout = Layout(
            Fieldset(
                _('Model upload form'),
                'model_name',
                'description',
                'upload_file',
                'organisation',
                'model_type',
            ),
        )
        submit = Submit('submit', _('Submit'), css_class='btn btn-primary')
        self.helper.add_input(submit)
        super(ModelUploadForm, self).__init__(*args, **kwargs)
