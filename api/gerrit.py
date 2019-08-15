#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-03 14:42:49
# @Author  : Shanming Liu

from .utils import helper
from .utils import uri
from .changes import Change, Revision
from .projects import Project
from .groups import Group
from .accounts import Account
from .utils.exceptions import GerritError


class Gerrit(object):
    """docstring for Gerrit"""

    def __init__(self, baseurl, username=None,
                 password=None, level='INFO'):
        """
        :param url: baseurl for gerrit instance including port, str
        :param username: username for Gerrit
        :param password: password or http token for Gerrit
        :param level: log level for logging
        :return: a Gerrit obj
        """
        self.baseurl = baseurl.rstrip('/')
        self.username = username
        self.password = password
        self.logger = logger = helper.get_logger('Gerrit', level)
        self.session = helper.GerritSession(username, password, logger=logger)

    def changes(self, query=None, limit=None, option=None,
                ret_type=False):
        url = self.baseurl + uri.Changes
        params = {
            'q': query,
            'n': limit,
            'o': option
        }
        resp = self.session.get(url, params=params)
        if ret_type:
            return [Change(self, item['change_id']) for item in resp]
        return resp

    def change(self, change_id):
        return Change(self, change_id=change_id)

    def revision(self, change_id, revision_id):
        return Revision(self, Change(self, change_id), revision_id)

    def get_revision(self, commit):
        changes = self.changes("commit:%s" % commit, ret_type=True)
        if len(changes) != 1:
            err_msgs = ["Found changes with revision[%s] not unique," % commit,
                        "Please double check your revision."]
            raise GerritError(' '.join(err_msgs))
        return changes[0].revision(commit)

    def projects(self, query='', start=0, limit=None,
                 ret_type=False):
        url = self.baseurl + uri.Projects
        params = {
            'query': query,
            'start': start,
            'limit': limit
        }
        resp = self.session.get(url, params=params)
        if ret_type:
            return [Project(self, name) for name in resp]
        return resp

    def project(self, name):
        return Project(self, name)

    def version(self):
        url = self.baseurl + uri.ServerVersion
        return self.session.get(url)

    def server_info(self):
        url = self.baseurl + uri.ServerInfo
        return self.session.get(url)

    def commit_msg_hook(self):
        url = self.baseurl + uri.CommitMsgHook
        return self.session.get(url)

    def groups(self, query='', start=0, limit=None,
               ret_type=False):
        """Lists the groups accessible by the caller."""
        url = self.baseurl + uri.Groups
        params = {
            'query2': query,
            'start': start,
            'limit': limit
        }

        resp = self.session.get(url, params=params)
        if ret_type:
            return [Group(self, item['group_id']) for item in resp]
        return resp

    def group(self, group_id):
        return Group(self, group_id)

    def create_group(self, group_name,
                     description='',
                     visiable_to_all=True, owner_id=None):
        """Creates a new Gerrit internal group."""
        data = {
            "description": description,
            "visible_to_all": visiable_to_all,
            "owner_id": owner_id
        }
        url = self.baseurl + uri.Group.format(group_id=group_name)
        resp = self.session.put(url, json=data)
        return Group(self, resp['group_id'])

    def accounts(self, query='', limit=None, option=None,
                 ret_type=False):
        """Queries accounts visible to the caller."""
        url = self.baseurl + uri.Accounts
        params = {
            'q': query,
            'n': limit,
            'o': option
        }

        resp = self.session.get(url, params=params)
        if ret_type:
            return [Account(self, item['_account_id']) for item in resp]
        return resp

    def account(self, account_id):
        return Account(self, account_id)

    def create_account(self, username, **data):
        url = self.baseurl + uri.Account.format(account_id=username)
        resp = self.session.put(url, json=data)
        return Account(self, resp['_account_id'])

    def owner(self):
        return Account(self, 'self')
