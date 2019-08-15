#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-03 14:42:49
# @Author  : Shanming Liu

# Changes start
Changes = '/a/changes/'
Change = '/a/changes/{change_id}'
Reviewer = '/a/changes/{change_id}/reviewers/{account_id}'
Revision = '/a/changes/{change_id}/revisions/{revision_id}'
# Changes end

# Projects start
Projects = '/a/projects/'
Project = '/a/projects/{project_name}'
Branchs = '/a/projects/{project_name}/branches/'
Branch = '/a/projects/{project_name}/branches/{branch_name}'
Tags = '/a/projects/{project_name}/tags/'
Tag = '/a/projects/{project_name}/tags/{tag_id}'
# Project end

# Group start
Groups = '/a/groups/'
Group = '/a/groups/{group_id}'
# Group end

# Account start
Accounts = '/a/accounts/'
Account = '/a/accounts/{account_id}'
# Account end

# Hooks start
CommitMsgHook = '/tools/hooks/commit-msg'
# Hooks end

# Config start
ServerVersion = '/config/server/version'
ServerInfo = '/config/server/info'
# Config end
