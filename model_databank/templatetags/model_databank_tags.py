from django import template
from django.contrib.auth.models import User
from django.template import Node, TemplateSyntaxError


from model_databank.conf import settings
from model_databank.vcs_utils import get_last_update_date

register = template.Library()


class MercurialCommitNode(Node):
    """Return the Mercurial page URL for the requested commit."""
    def __init__(self, model_reference, log_entry):
        self.model_reference = model_reference
        self.log_entry = log_entry

    def render(self, context):
        model_reference = self.model_reference.resolve(context)
        log_entry = self.log_entry.resolve(context)
        # remove trailing slash, if any
        url_root = settings.MODEL_DATABANK_REPOSITORY_URL_ROOT.strip('/')
        return '/'.join([url_root, model_reference.slug, 'rev',
                         log_entry['node']])


@register.tag
def mercurial_commit_url(parser, token):
    """
    Return an absolute Mercurial commit URL matching given model reference
    and log entry data.

    """
    bits = token.split_contents()
    if len(bits) < 3:
        raise TemplateSyntaxError("'%s' takes at least two arguments"
                                  " (a model reference and a log entry)" %
                                  bits[0])
    model_reference = parser.compile_filter(bits[1])
    log_entry = parser.compile_filter(bits[2])

    return MercurialCommitNode(model_reference, log_entry)


@register.filter
def pretty_user(user):
    """
    Filter for pretty printing user instances. Checks for first and last name
    and uses those if available. Falls back on username.

    """
    if not isinstance(user, User):
        raise TemplateSyntaxError("pretty_user filter expects an "
                                  "django.contrib.auth.models.USer instance")
    if user.first_name and user.last_name:
        return user.get_full_name()
    else:
        return user.username


@register.filter
def last_update_date(model_reference):
    return model_reference.last_repo_update
