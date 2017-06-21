# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext as _

import requests
import six

logger = logging.getLogger(__name__)


class RoleRequiredRemoteMixin(AccessMixin):
    """
    Subclass of AccessMixin that fetches permission info from a remote 3Di
    permissions API.

    """
    raise_exception = True
    permission_denied_message = _(
        "You're not allowed to see this page. Contact your administrator to "
        "request access permission.")
    role_required = None  # can be a string or a list of strings

    def get_role_required(self):
        """
        Must return an iterable of role strings.

        Optionally, override this method to override the role_required
        attribute.
        """
        if not self.role_required:
            raise ImproperlyConfigured(
                '{0} is missing the role attribute. Define {0}.role, or '
                'override {0}.get_role_required().'.format(
                    self.__class__.__name__)
            )
        if isinstance(self.role_required, six.string_types):
            roles = (self.role_required,)
        else:
            roles = self.role_required
        return roles

    def has_role(self):
        """
        check whether the user has the required role

        :returns bool. If True it also puts all organisations for which
            the user has the required role into the session dict
        """
        organisations = set()
        roles = self.get_role_required()
        for role in roles:
            permissions_api_url = '{}{}/{}/'.format(
                settings.PERMISSIONS_API_URL,
                self.request.user.username, role)
            try:
                # get the organisation ids for the username / role combo
                resp = requests.get(permissions_api_url)
            except requests.RequestException:
                logger.exception(
                    "Error calling permissions api url: %s",
                    permissions_api_url)
                continue
            else:
                if resp.ok:
                    # add the organisation ids from the response
                    organisations.update(resp.json())
                else:
                    logger.error(
                        "Error calling permissions api url: %s, status code: "
                        "%s, reason: %s", permissions_api_url,
                        resp.status_code, resp.reason)
        # convert organisations to a list, otherwise it won't be serializable
        organisations = list(organisations)

        if not organisations:
            # no organisations returned for the required role(s)
            return False
        else:
            # put the organisations in the session
            self.request.session['organisations'] = organisations
            return True

    def dispatch(self, request, *args, **kwargs):
        if not self.has_role():
            return self.handle_no_permission()
        return super(RoleRequiredRemoteMixin, self).dispatch(
            request, *args, **kwargs)
