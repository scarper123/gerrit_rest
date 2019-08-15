#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-03 14:42:49
# @Author  : Shanming Liu

import weakref

from .utils import helper
from .utils import uri


class Revision(helper.GerritMixin):
    """docstring for Revision"""

    def __init__(self, gerrit, change, revision_id):
        super().__init__(gerrit,
                         uri.Revision.format(change_id=change.change_id,
                                             revision_id=revision_id))
        self.change = weakref.proxy(change)
        self.revision_id = revision_id

    def commit(self):
        """Retrieves a parsed commit of a revision."""
        url = self.baseurl + '/commit'
        return self.session.get(url)

    def description(self):
        """Retrieves the description of a patch set."""
        url = self.baseurl + '/description'
        return self.session.get(url)

    def set_description(self, description=''):
        """Sets the description of a patch set."""
        url = self.baseurl + '/description'
        return self.session.put(url, data={'description': description})

    def merge_list(self):
        """Returns the list of commits that are being
        integrated into a tarsession.get branch by a merge commit."""
        url = self.baseurl + '/mergelist'
        return self.session.get(url)

    def actions(self):
        """Retrieves revision actions of the revision of a change."""
        url = self.baseurl + '/actions'
        return self.session.get(url)

    def review(self):
        """Retrieves a review of a revision."""
        url = self.baseurl + '/review'
        return self.session.get(url)

    def related_changes(self):
        """Retrieves related changes of a revision.
        Related changes are changes that either depend on,
        or are dependencies of the revision."""
        url = self.baseurl + '/related'
        return self.session.get(url)

    def set_review(self, message='', tag=None, labels=None):
        """Sets a review on a revision.
        https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#set-review"""
        url = self.baseurl + '/review'
        data = {
            'message': message,
            'tag': tag,
            'labels': labels
        }

        return self.session.post(url, json=data)

    def rebase(self, base=None):
        """Rebases a revision."""
        url = self.baseurl + '/rebase'
        data = {
            'base': base
        } if base else None
        return self.session.post(url, json=data)

    def submit(self):
        """Submits a revision."""
        url = self.baseurl + '/submit'
        return self.session.post(url)

    def publish(self):
        """Publishes a draft revision."""
        url = self.baseurl + '/publish'
        return self.session.post(url)

    def delete(self):
        """session.deletes a draft revision."""
        return self.session.delete(self.baseurl)

    def patch(self):
        """session.gets the formatted patch for one revision."""
        url = self.baseurl + '/patch'
        return self.session.get(url)

    def mergeable(self, other=False):
        """Gets the method the server will use to submit (merge)
        the change and an indicator if the change is currently mergeable."""
        url = self.baseurl + '/mergeable'
        if other:
            url = '%s?other-branches' % url
        return self.session.get(url)

    def submit_type(self):
        """Gets the method the server will use to submit (merge) the change."""
        url = self.baseurl + '/submit_type'
        return self.session.get(url)

    def drafts(self):
        """Lists the draft comments of a revision
        that belong to the calling user."""
        url = self.baseurl + '/drafts'
        return self.session.get(url)

    def files(self, reviewed=False):
        """Lists the files that were modified,
        added or deleted in a revision."""
        url = self.baseurl + '/files'
        if reviewed:
            url = '%s?reviewed' % url
        return self.session.get(url)

    def __repr__(self):
        return '<Revision %s>' % self.revision_id


class Change(helper.GerritMixin):
    """docstring for ChangeNew"""

    def __init__(self, gerrit, change_id):
        super().__init__(gerrit, uri.Change.format(change_id=change_id))
        self.change_id = change_id

    def merge(self, patchSet):
        url = self.baseurl + '/merge'
        return self.session.post(url, data=patchSet)

    def detail(self, o=None):
        url = self.baseurl + '/detail'
        params = {'o': o} if o else None
        return self.session.get(url, params=params)

    def topic(self):
        url = self.baseurl + '/topic'
        return self.session.get(url)

    def set_topic(self, topic=''):
        url = self.baseurl + '/topic'
        return self.session.put(url, data={'topic': topic})

    def delete_topic(self):
        url = self.baseurl + '/topic'
        return self.session.delete(url)

    def assignee(self):
        url = self.baseurl + '/assignee'
        return self.session.get(url)

    def set_assignee(self, assignee=''):
        url = self.baseurl + '/assignee'
        return self.session.put(url, data={'assignee': assignee})

    def anandon(self, message='', notify=''):
        url = self.baseurl + '/abandon'
        data = {
            'message': message,
            'notify': notify,
        }
        return self.session.post(url, data=data)

    def restore(self, message=''):
        url = self.baseurl + '/restore'
        data = {
            'message': message
        }
        return self.session.post(url, data=data)

    def rebase(self, base=None):
        """Rebases a change.

        base: optional: The new parent revision.
            This can be a ref or a SHA1 to a concrete patchset.
        """
        url = self.baseurl + '/rebase'
        data = {
            'base': base
        } if base else None
        return self.session.post(url, data=data)

    def revert(self, message=''):
        url = self.baseurl + '/revert'
        data = {
            'message': message
        }
        return self.session.post(url, data=data)

    def submit(self):
        url = self.baseurl + '/submit'
        return self.session.post(url)

    def publish(self):
        url = self.baseurl + '/publish'
        return self.session.post(url)

    def delete(self):
        return self.session.delete(self.baseurl)

    def comments(self):
        """Lists the published comments of all revisions of the change.
        """
        url = self.baseurl + '/comments'
        return self.session.get(url)

    def drafts(self):
        """Lists the draft comments of all revisions of
        the change that belong to the calling user.
        """
        url = self.baseurl + '/drafts'
        return self.session.get(url)

    def check(self):
        """Performs consistency checks on the change,
        and returns a ChangeInfo entity with the problems field."""
        url = self.baseurl + '/check'
        return self.session.get(url)

    def reviewers(self):
        """Lists the reviewers of a change."""
        url = self.baseurl + '/reviewers'
        return self.session.get(url)

    def revision(self, revision_id):
        """session.get a revision."""
        return Revision(self.gerrit, self, revision_id)

    def __repr__(self):
        return '<Change %s>' % self.change_id
