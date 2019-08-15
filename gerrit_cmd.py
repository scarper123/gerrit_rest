#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-08-16 14:22:16
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import pathlib
import json
import sys

import yaml
import fire
import tabulate

from api import Gerrit, GerritError

BASEDIR = pathlib.Path(__file__).parent


def get_config():
    config_file = BASEDIR / 'config/gerrit.json'
    return json.load(config_file.open())


def format_output(data, fmt_type='JSON'):
    if fmt_type == "JSON":
        data = json.dumps(data)
    elif fmt_type == "YAML":
        data = yaml.safe_dump(data)

    return data


class GerritCmd(object):
    def __init__(self, fmt_type='YAML', debug=False):
        """
        Gerrit central restful api wrappered command list.
        Tips:
            1. When input arguments use dot, it will convert to dict
            2. When input arguments use strike, it will convert to underline.
        :param fmt_type: Output format
        :param debug: Set logging level to DEBUG
        """
        config = get_config()
        self.gerrit = Gerrit(config['baseurl'],
                             config['username'],
                             config['password'],
                             level='DEBUG' if debug else 'INFO')
        self.fmt_type = fmt_type

    def query(self, query=None, limit=None, option=None):
        """
        Fetch query result.
        :param query: Query string
        :param limit: Limit the returned results.
        :param option: Additional fields can be obtained by adding o parameters
        """
        resp = self.gerrit.changes(query, limit, option)
        output = format_output(resp, self.fmt_type)
        print(output)

    def query_commit_files(self, commit):
        """
        Query gerrit central commit change files
        :param commit: Commit hash
        :return: list of commit change files
        """
        try:
            revision = self.gerrit.get_revision(commit)
        except GerritError as e:
            print('Error: %s' % str(e))
            sys.exit(1)
        file_list = revision.files()
        for name in file_list.keys():
            print(name)

    def query_change(self, change_id, **params):
        """
        Query gerrit central change id merge status
        :param change_id: ChangeId
        :return: change status
        """
        resp = self.gerrit.change(change_id).info(**params)
        output = format_output(resp, self.fmt_type)
        print(output)

    def query_change_files(self, change_id):
        """
        Fetch all files from change id,
         and verify the file name valid character.
        :param change_id: ChangeId
        :return: Sorted file names
        """
        change = self.gerrit.change(change_id)
        resp = change.info(o=["CURRENT_REVISION",
                              "CURRENT_FILES"])
        current_revision = resp['current_revision']
        file_list = resp['revisions'][current_revision]['files']
        for name in file_list.keys():
            print(name)

    def set_review(self, revision_id,
                   message='',
                   code_review=0,
                   verified=0,
                   command=None):
        """
        Set revision message
        :param revision_id: Gerrit change revision ID
        :param command: sub command after set review,
        if not set it just set review info.
            eg: ['rebase','submit','publish','delete']
        :param kwargs: review optional args.
        """
        revision = self.gerrit.get_revision(revision_id)
        labels = {}
        if code_review:
            labels['Code-Review'] = code_review
        if verified:
            labels['Verified'] = verified
        try:
            resp = revision.set_review(message=message,
                                       labels=labels)
            assert labels == resp['labels']
            if command and getattr(revision, command):
                getattr(revision, command)()
        except (GerritError, AssertionError):
            print('Set review failed')
            sys.exit(1)

    def create_branch(self, project_name, branch_name, revision=None):
        """
        Create branch on project.
        :param project_name: The name of the project.
        :param branch_name: The name of a branch or HEAD.
         The prefix refs/heads/ can be omitted.
        :param revision: optional, The base revision of the new branch.
         If not set, HEAD will be used as base revision.
        """

        project = self.gerrit.project(project_name)
        msg = 'Create branch[%s] on project[%s] ' % (branch_name, project_name)

        try:
            project.create_branch(branch_name, revision)
        except GerritError:
            print(msg + 'failed')
            sys.exit(1)
        else:
            print(msg + 'successful')

    def delete_branch(self, project_name, branch_name):
        """
        Delete branch on project.
        :param project_name: The name of the project.
        :param branch_name: The name of a branch or HEAD.
         The prefix refs/heads/ can be omitted.
        :return: No content
        """
        project = self.gerrit.project(project_name)
        msg = 'Delete branch[%s] on project[%s] ' % (branch_name, project_name)
        try:
            project.branch(branch_name).delete()
        except GerritError:
            print(msg + 'failed')
            sys.exit(1)
        else:
            print(msg + 'successful')

    def ls_members(self, group_name):
        group = self.gerrit.groups(query='name:{}'.format(group_name),
                                   ret_type=True)[0]
        members = group.members()
        names = ['id', 'username', 'full name', 'email']
        fields = ['_account_id', 'username', 'name', 'email']
        table_rows = [[row[i] for i in fields] for row in members]
        print(tabulate.tabulate(table_rows, headers=names, tablefmt='plain'))

    def version(self):
        print(self.gerrit.version())

    def commit_msg_hook(self, path='.'):
        """
        Download gerrit commit-msg hook, and save it into file if path exist.
        :param path: File path to save commit-msg hook.
        """

        dst_path = pathlib.Path(path)
        if dst_path.is_file():
            # not change the default path
            pass
        else:
            if not dst_path.exists():
                dst_path.mkdir(parents=True, exist_ok=True)
            dst_path = dst_path / 'commit-msg'
        print('Download commit-msg hook into %s' % str(dst_path))
        with dst_path.open('wt') as out_file:
            resp = self.gerrit.commit_msg_hook()
            out_file.write(resp)

        # change file to executable permission
        dst_path.chmod(0o770)

    def check_patch_is_draft(self, change_id, ref_spec):
        resp = self.gerrit.change(change_id).info(o='ALL_REVISIONS')
        latest_rev = resp['current_revision']
        for rev, item in resp['revisions'].items():
            if ref_spec == item['ref']:
                if 'draft' in item:
                    print('THIS IS A DRAFT, ABORT')
                    sys.exit(1)
                # match the ref and not found 'draft'
                if rev != latest_rev:
                    print("THIS PATCH REVISION IS NOT LATEST")
                    sys.exit(1)
                break
        else:
            print('Not found this ref[%s]' % ref_spec)
            sys.exit(1)

    def check_patch_is_mergeable(self, revision_id):
        revision = self.gerrit.get_revision(revision_id)
        merge_info = revision.mergeable()
        if not merge_info['mergeable']:
            print('Revision[%s] can not be merged' % revision_id)
            sys.exit(1)
        print('Revision[%s] can be merged' % revision_id)


def main():
    fire.Fire(GerritCmd)


if __name__ == '__main__':
    main()
