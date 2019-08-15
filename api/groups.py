#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-03 14:42:49
# @Author  : Shanming Liu

from .utils import helper
from .utils import uri
from .accounts import Account


class Group(helper.GerritMixin):
    def __init__(self, gerrit, group_id):
        super().__init__(gerrit, uri.Group.format(group_id=group_id))
        self.group_id = group_id

    def detail(self):
        """Retrieves a group with the
         direct members and the directly included groups."""
        url = self.baseurl + '/detail'
        return self.session.get(url)

    def name(self):
        """Retrieves the name of a group."""
        url = self.baseurl + '/name'
        return self.session.get(url)

    def rename(self, name):
        """Renames a Gerrit internal group."""
        url = self.baseurl + '/name'
        data = {
            'name': name
        }
        return self.session.put(url, json=data)

    def description(self):
        """Retrieves the description of a group."""
        url = self.baseurl + '/description'
        return self.session.get(url)

    def set_description(self, description):
        """Sets the description of a Gerrit internal group."""
        url = self.baseurl + '/description'
        data = {
            'description': description
        }
        return self.session.put(url, json=data)

    def delete_description(self):
        """Deletes the description of a Gerrit internal group."""
        url = self.baseurl + '/description'
        return self.session.delete(url)

    def options(self):
        """Retrieves the options of a group."""
        url = self.baseurl + '/options'
        return self.session.get(url)

    def set_options(self, **options):
        """Sets the options of a Gerrit internal group."""
        url = self.baseurl + '/options'
        return self.session.put(url, json=options)

    def owner(self):
        """Retrieves the owner group of a Gerrit internal group."""
        url = self.baseurl + '/owner'
        return self.session.get(url)

    def set_owner(self, owner_id):
        """Sets the owner group of a Gerrit internal group."""
        url = self.baseurl + '/owner'
        data = {
            "owner": owner_id
        }
        return self.session.put(url, json=data)

    def members(self, recursive=False, ret_type=False):
        """Lists the direct members of a Gerrit internal group. """
        url = self.baseurl + '/members'
        if recursive:
            url += '?recursive'
        resp = self.session.get(url)
        if ret_type:
            account_ids = sorted(map(lambda x: x['_account_id'], resp))
            return [Account(self.gerrit, _id) for _id in account_ids]
        return resp

    def account(self, account_id):
        """Retrieves a group member."""
        return Account(self.gerrit, account_id)

    def add_member(self, account_id):
        """Adds a user as member to a Gerrit internal group."""
        url = self.baseurl + '/members/{}'.format(account_id)
        return self.session.put(url)

    def add_members(self, *members):
        """Adds a user as member to a Gerrit internal group."""
        url = self.baseurl + '/members'
        data = {
            "members": members
        }
        return self.session.put(url, json=data)

    def remove_member(self, account_id):
        url = self.baseurl + '/members/{}'.format(account_id)
        return self.session.delete(url)

    def groups(self):
        """Lists the direct subgroups of a group."""
        url = self.baseurl + '/groups/'
        resp = self.session.get(url)
        return [Group(self.gerrit, item['group_id']) for item in resp]

    def __repr__(self):
        return '<Group %s>' % self.group_id
