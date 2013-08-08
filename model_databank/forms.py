from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit


class NewModelUploadForm(forms.Form):
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

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.html5_required = True
        self.helper.layout = Layout(
            Fieldset(
                _('Model upload form'),
                'model_name',
                'description',
                'upload_file',
            ),
        )
        submit = Submit('submit', _('Submit'), css_class='btn btn-primary')
        self.helper.add_input(submit)
        super(NewModelUploadForm, self).__init__(*args, **kwargs)


class UploadForm(forms.Form):
    """Model for uploading zipped models."""
    upload_file = forms.FileField(required=True)
    description = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                'Model upload form',
                'description',
                'upload_file',
            ),
        )
        submit = Submit('submit', _('Submit'), css_class='btn btn-primary')
        self.helper.add_input(submit)
        super(UploadForm, self).__init__(*args, **kwargs)
