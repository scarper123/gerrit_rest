#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-04 14:10:35
# @Author  : Shanming Liu

import collections
import json
import logging
import pathlib
import sys
import requests
import urllib.parse as urlparse
import weakref

from .exceptions import GerritError

# requests.urllib3.disable_warnings()


def get_logger(name, level=logging.DEBUG,
               stream=None, filename=None,
               fmt_str=None, date_str=None):
    if fmt_str is None:
        fmt_str = "<%(asctime)s> [%(name)s] [%(levelname)s] %(message)s"
    if date_str is None:
        date_str = '%Y-%m-%d %H:%M:%S'

    log = logging.getLogger(name)
    log.setLevel(level)

    log_fmt = logging.Formatter(fmt_str,
                                datefmt=date_str)

    if stream is None:
        stream = sys.__stdout__

    handler = logging.StreamHandler(stream)
    handler.setFormatter(log_fmt)
    log.addHandler(handler)

    if filename and pathlib.Path(filename).exists():
        handler = logging.FileHandler(filename, 'wt')
        handler.setFormatter(log_fmt)
        log.addHandler(handler)

    return log


def infinite_dict():
    return collections.defaultdict(infinite_dict)


def expand_dot_dict(data, res=None):
    """
    Expand dict keys with dot to more levels dict
    :param data: dict data
    :param res: more levels data
    :Example:
        >>> expand_dot_dict({'a.b.c.d': 10,
                        'a.b.c.e': 20,
                        'a.b.e': 30})
        >>> {'a': {'b': {'c': {'d': 10,
                   'e': 20},
             'e': 30}}}
    """
    if res is None:
        res = dict()
    for key, value in data.items():
        if '.' in key:
            index = key.index('.')
            sub_key = key[:index]
            res[sub_key] = expand_dot_dict(
                {key[index + 1:]: value}, res.get(sub_key))
        else:
            res[key] = value

    return res


class GerritSession(requests.Session):
    """docstring for GerritSession"""

    def __init__(self, username, password, timeout=10, logger=None):
        super(GerritSession, self).__init__()
        self.auth = requests.auth.HTTPBasicAuth(username, password)
        # self.headers["Content-Type"] = "application/json; charset=UTF-8"
        # self.verify = False

        self.timeout = timeout
        self.logger = logger if logger else get_logger('GerritSession')

    def prepare_request(self, request):
        if request.params:
            # remove not exists value from params
            params = request.params
            if hasattr(params, "items"):
                params = params.items()
            params = [(k, v) for k, v in params if v]
            request.params = urlparse.urlencode(params,
                                                doseq=True,
                                                safe='+')
        return super().prepare_request(request)

    def send(self, request, **kwargs):
        self.logger.debug('Send %s request: %s',
                          request.method, request.url)
        kwargs.setdefault('timeout', self.timeout)
        resp = super().send(request, **kwargs)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            self.logger.error('Error: %s', str(e))
            self.logger.error('Reason: %s', e.response.text)
            raise GerritError(e.response.text)
        try:
            content = resp.text.lstrip(")]}'")
            return json.loads(content)
        except json.JSONDecodeError:
            return resp.text


class GerritMixin(object):
    """docstring for GerritMixin"""

    def __init__(self, gerrit, url_path):
        self.gerrit = gerrit
        self.baseurl = urlparse.urljoin(gerrit.baseurl, url_path)
        self.session = weakref.proxy(gerrit.session)
        self.logger = weakref.proxy(gerrit.logger)

    def info(self, **params):
        params = [(k, v) for k, v in params.items() if v]
        return self.session.get(self.baseurl,
                                params=params)
