from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit


class NewModelUploadForm(forms.Form):
    """Model for uploading new zipped model files."""
    upload_file = forms.FileField(required=True)
    model_name =forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                'New model upload form',
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
