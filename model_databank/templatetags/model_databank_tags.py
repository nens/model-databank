from django import template
from django.template import Node, TemplateSyntaxError

from model_databank.conf import settings

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
