#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-03 14:42:49
# @Author  : Shanming Liu


from .utils import helper
from .utils import uri

"""This page describes the account related REST endpoints.
"""


class Account(helper.GerritMixin):
    """Gerrit Account"""

    def __init__(self, gerrit, account_id):
        super().__init__(gerrit,
                         uri.Account.format(account_id=account_id))
        self.account_id = account_id

    def details(self):
        """
        Retrieves the details of an account
        """
        url = self.baseurl + '/detail'
        return self.session.get(url)

    def name(self):
        """
        Retrieves the full name of an account.
        If the account does not have a name an empty string is returned.
        """
        url = self.baseurl + '/name'
        return self.session.get(url)

    def set_name(self, name=''):
        """
        Sets the full name of an account.
        """
        url = self.baseurl + '/name'
        data = {
            'name': name
        }
        return self.session.put(url, json=data)

    def delete_name(self,):
        """
        Deletes the name of an account.
        """
        url = self.baseurl + '/name'
        return self.session.delete(url)

    def status(self):
        """
        Retrieves the status of an account.
        If the account does not have a status an empty string is returned.
        request endpoint: /a/accounts/{account_id}/status
        """
        url = self.baseurl + '/status'
        return self.session.get(url)

    def set_status(self, status=''):
        """
        Sets the status of an account.
        request type: PUT
        request endpoint: /a/accounts/{account_id}/status
        """
        url = self.baseurl + '/status'
        data = {
            'status': status
        }
        return self.session.put(url, json=data)

    def username(self):
        """
        Retrieves the username of an account.
        If the account does not have a username
the response is “404 Not Found”.
        request type: GET
        request endpoint: /a/accounts/{account_id}/username
        """
        url = self.baseurl + '/username'
        return self.session.get(url)

    def set_username(self, username):
        """
        The new username must be provided in the request body inside
a UsernameInput entity.
Once set, the username cannot be changed or deleted.
If attempted this fails with “405 Method Not Allowed”.
As response the new username is returned.
        request name: SetUsername
        request type: PUT
        request endpoint: /a/accounts/{account_id}/username
        """
        url = self.baseurl + '/username'
        data = {
            'username': username
        }
        return self.session.put(url, json=data)

    def active(self):
        """
        Checks if an account is active.
        If the account is active the string ok is returned.
        If the account is inactive the response is “204 No Content”.
        request type: GET
        request endpoint: /a/accounts/{account_id}/active
        """
        url = self.baseurl + '/active'
        return self.session.get(url)

    def set_active(self):
        """
        Sets the account state to active.
        If the account was already active the response is “200 OK”.
        request type: PUT
        request endpoint: /a/accounts/{account_id}/active
        """
        url = self.baseurl + '/active'
        return self.session.put(url)

    def delete_active(self,):
        """
        Sets the account state to inactive.
        If the account was already inactive the response is “409 Conflict”.
        request type: DELETE
        request endpoint: /a/accounts/{account_id}/active
        """
        url = self.baseurl + '/active'
        return self.session.delete(url)

    def set_http_password(self, generate=True):
        """
        Sets/Generates the HTTP password of an account.
        request type: PUT
        request endpoint: /a/accounts/{account_id}/password.http
        """
        url = self.baseurl + '/password.http'
        data = {
            "generate": generate
        }
        return self.session.put(url, json=data)

    def delete_http_password(self,):
        """
        Deletes the HTTP password of an account.
        request type: DELETE
        request endpoint: /a/accounts/{account_id}/password.http
        """
        url = self.baseurl + '/password.http'
        return self.session.delete(url)

    def get_oauth_access_token(self):
        """
        Returns a previously obtained OAuth access token.
        request type: GET
        request endpoint: /a/accounts/{account_id}/oauthtoken
        """
        url = self.baseurl + '/oauthtoken'
        return self.session.get(url)

    def emails(self):
        """
        Returns the email addresses that are configured for the specified user.
        request type: GET
        request endpoint: /a/accounts/{account_id}/emails
        """
        url = self.baseurl + '/emails'
        return self.session.get(url)

    def ssh_keys(self):
        """
        Returns the SSH keys of an account.
        request type: GET
        request endpoint: /a/accounts/{account_id}/sshkeys
        """
        url = self.baseurl + '/sshkeys'
        return self.session.get(url)

    def add_ssh_Key(self, ssh_key):
        """
        Adds an SSH key for a user.
        The SSH public key must be provided as raw content in the request body.
        request type: POST
        request endpoint: /a/accounts/{account_id}/sshkeys
        """
        url = self.baseurl + '/sshkeys'
        data = ssh_key
        return self.session.post(url,
                                 data=data,
                                 headers={'Content-Type': 'plain/text'})

    def delete_ssh_key(self, ssh_key_id):
        """
        Deletes an SSH key of a user.
        request type: DELETE
        request endpoint: /a/accounts/{account_id}/sshkeys/{ssh_key_id}
        """
        url = self.baseurl + '/sshkeys/{}'.format(ssh_key_id)
        return self.session.delete(url)

    def gpg_keys(self,):
        """
        Returns the GPG keys of an account.
        request type: GET
        request endpoint: /a/accounts/{account_id}/gpgkeys
        """
        url = self.baseurl + '/gpgkeys'
        return self.session.get(url)

    def get_gpg_key(self, gpg_key_id):
        """
        Retrieves a GPG key of a user.
        request type: GET
        request endpoint: /a/accounts/{account_id}/gpgkeys/{gpg_key_id}
        """
        url = self.baseurl + '/gpgkeys/{}'.format(gpg_key_id)
        return self.session.get(url)

    def delete_gpg_key(self, gpg_key_id):
        """
        Deletes a GPG key of a user.
        request type: DELETE
        request endpoint: /a/accounts/{account_id}/gpgkeys/{gpg_key_id}
        """
        url = self.baseurl + '/gpgkeys/{}'.format(gpg_key_id)
        return self.session.delete(url)

    def capabilities(self):
        """Returns the global capabilities that are enabled for the specified user.
        request type: GET
        request endpoint: /a/accounts/{account_id}/capabilities
        """
        url = self.baseurl + '/capabilities'
        return self.session.get(url)

    def check_capability(self, capability_id):
        """
        Checks if a user has a certain global capability.
If the user has the global capability the string ok is returned.
If the user doesn’t have the global capability the response is “404 Not Found”.
        request type: GET
        request endpoint: /a/accounts/{account_id}/capabilities/{capability_id}
        """
        url = self.baseurl + '/capabilities/{}'.format(capability_id)
        return self.session.get(url)

    def groups(self, ret_type=False):
        """
        Lists all groups that contain the specified user as a member.
        request type: GET
        request endpoint: /a/accounts/{account_id}/groups/
        """
        url = self.baseurl + '/groups'
        resp = self.session.get(url)
        if ret_type:
            from .groups import Group
            groups = filter(lambda x: 'group_id' in x, resp)
            group_ids = sorted(map(lambda x: x['group_id'], groups))
            return [Group(self.gerrit, gid) for gid in group_ids]
        return resp

    def preferences(self,):
        """
        Retrieves the user’s preferences.
        request type: GET
        request endpoint: /a/accounts/{account_id}/preferences
        """
        url = self.baseurl + '/preferences'
        return self.session.get(url)

    def set_preferences(self, **data):
        """
        Sets the user’s preferences.
        request type: PUT
        request endpoint: /a/accounts/{account_id}/preferences
        """
        url = self.baseurl + '/preferences'
        return self.session.put(url, json=data)

    def watched_projects(self,):
        """
        Retrieves all projects a user is watching.
        request type: GET
        request endpoint: /a/accounts/{account_id}/watched.projects
        """
        url = self.baseurl + '/watched.projects'
        return self.session.get(url)

    def __repr__(self):
        return '<Account %s>' % self.account_id
