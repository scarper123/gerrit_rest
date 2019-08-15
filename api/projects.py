#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-03 14:42:49
# @Author  : Shanming Liu

import weakref

from .utils import uri
from .utils import helper


class Branch(helper.GerritMixin):
    def __init__(self, gerrit, project, branch_name=None):
        if 'refs/' in branch_name:
            self.ref = branch_name
            branch_name = branch_name.split('/')[-1]
        else:
            self.ref = 'refs/heads/{}'.format(branch_name)
        super().__init__(gerrit, uri.Branch.format(
            project_name=project.project_name,
            branch_name=branch_name))
        self.project = weakref.proxy(project)
        self.branch_name = branch_name

    def create(self, revision=None):
        data = {
            'revision': revision
        } if revision else None
        return self.session.put(self.baseurl, json=data)

    def delete(self):
        return self.session.delete(self.baseurl)

    def mergeable(self, source, strategy=None):
        """Gets whether the source is mergeable with the target branch."""
        url = self.baseurl + '/mergeable'
        param = {
            'source': source,
        }
        if strategy:
            param['strategy'] = strategy
        return self.session.get(url, param=param)

    def reflog(self):
        """Gets the reflog of a certain branch."""
        url = self.baseurl + '/reflog'
        return self.session.get(url)

    def __repr__(self):
        return '<Branch %s>' % self.ref


class Tag(helper.GerritMixin):
    """docstring for Tag"""

    def __init__(self, gerrit, project, tag_id):
        if 'refs/' in tag_id:
            tag_id = tag_id.split('/')[-1]
        super().__init__(gerrit,
                         uri.Tag.format(project_name=project.project_name,
                                        tag_id=tag_id))
        self.project = weakref.proxy(project)
        self.tag_id = tag_id

    def create(self, revision=None, message=None):
        data = {
            "revision": revision if not revision else 'HEAD'
        }
        if message:
            data['message'] = message
        return self.session.put(self.baseurl, json=data)

    def delete(self):
        return self.session.delete(self.baseurl)

    def __repr__(self):
        return '<Tag refs/tags/%s>' % self.tag_id


class Project(helper.GerritMixin):
    """This page describes the project related REST endpoints."""

    def __init__(self, gerrit, name):
        if '/' in name:
            name = name.replace('/', '%2F')
        super(Project, self).__init__(gerrit,
                                      uri.Project.format(project_name=name))
        self.project_name = name

    def create(self, data):
        pass

    def description(self):
        """Retrieves the description of a project."""
        url = self.baseurl + '/description'
        return self.session.get(url)

    def set_description(self, data=None):
        """Sets the description of a project.
        https://gerrit-review.googlesource.com/Documentation/rest-api-projects.html#set-project-description"""
        url = self.baseurl + '/description'
        return self.session.put(url, json=data)

    def delete_description(self):
        url = self.baseurl + '/description'
        return self.session.delete(url)

    def head(self):
        """Retrieves for a project the name
        of the branch to which HEAD points."""
        url = self.baseurl + '/HEAD'
        return self.session.get(url)

    def set_head(self, data):
        """Sets HEAD for a project.
        https://gerrit-review.googlesource.com/Documentation/rest-api-projects.html#set-head"""
        url = self.baseurl + '/HEAD'
        return self.session.put(url, json=data)

    def branches(self, **params):
        """List the branches of a project."""
        url = self.baseurl + '/branches'
        resp = self.session.get(url, params=params)
        return [Branch(self.gerrit, self, branch['ref']) for branch in resp]

    def create_branch(self, branch_name, revision=None):
        """Creates a new branch.
        https://gerrit-review.googlesource.com/Documentation/rest-api-projects.html#create-branch"""
        branch = Branch(self.gerrit, self, branch_name)
        branch.create(revision)
        return branch

    def delete_branchs(self, *branchs):
        """Delete one or more branches.
        https://gerrit-review.googlesource.com/Documentation/rest-api-projects.html#delete-branches"""
        url = self.baseurl + ':delete'
        data = {
            'branchs': branchs
        }
        return self.session.post(url, json=data)

    def branch(self, branch_name):
        return Branch(self.gerrit, self, branch_name)

    def children(self):
        """List the direct child projects of a project."""
        url = self.baseurl + '/children'
        resp = self.session.get(url)
        return [Project(self.gerrit, item['id']) for item in resp]

    def tags(self, **params):
        """List the tags of a project."""
        url = self.baseurl + '/tags'
        resp = self.session.get(url, params=params)
        return [Tag(self.gerrit, self, item['ref']) for item in resp]

    def tag(self, tag_id):
        """Retrieves a tag of a project."""
        return Tag(self.gerrit, self, tag_id)

    def delete_tags(self, *tags):
        """Delete one or more tags."""
        url = self.baseurl + '/tags'
        data = {
            'tags': tags
        }
        self.session.post(url, json=data)

    def __repr__(self):
        return '<Project %s>' % self.project_name
