# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from django.contrib.auth.models import User


class AuthBackend(object):
    """
    Custom authentication backend, because we don't want the SSO server to
    determine whether or not a user can see this portal's pages. That will be
    determined by the permissions API (whether the user has 'change_model'
    permissions.
    """
    def authenticate(self, request, username=None, password=None):
        """Authenticate a user based on username and password.

        Args:
            request: A Django HttpRequest instance
            username (str): The user name.
            password (str): The password.

        Returns:
            User: User instance if successfully authenticated, None otherwise.
        """
        # check for valid credentials via SSO
        login_valid = True
        if login_valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a new user. There's no need to set a password
                # because the password is checked against the SSO password via
                # _check_credentials.
                user = User(username=username)
                user.save()
            return user
        return None

    def get_user(self, user_id):
        """Get a user for the given user_id.

        Args:
            user_id (int): The primary key of the user.

        Returns:
            User instance: The return value. User instance if an instance was
                found for the given ``user_id``, None otherwise.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
