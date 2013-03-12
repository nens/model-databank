import os
import subprocess
from datetime import datetime

from BeautifulSoup import BeautifulSoup as Soup

from model_databank.conf import settings


def mercurial_date_to_datetime(date_str):
    """Convert Mercurial log date to datetime instance.

    Input format is something like 2013-03-11T16:28:17+01:00

    """
    year = int(date_str[:4])
    month = int(date_str[5:7])
    day = int(date_str[8:10])
    hour = int(date_str[11:13])
    minute = int(date_str[14:16])
    second = int(date_str[17:19])
    # TODO: parse timezone
    dt = datetime(year, month, day, hour, minute, second)
    return dt


class MercurialLogData(object):
    """Mercurial XML log parser.

    Return a list of log entry dicts. These dicts contain these keywords:
      - node
      - revision
      - author_name
      - author_email
      - date
      - message (commit message)
      - paths:
        - path (path to file)
        - action ('A', 'M')

    """
    def __init__(self, xml):
        soup = Soup(xml)
        self.log_data = []
        for logentry in soup.findAll('logentry'):
            # node and revision
            log_dict = dict(logentry.attrs)
            log_dict['short_revision'] = log_dict['node'][:10]

            # tag
            tag_tag = logentry.find('tag')
            if tag_tag:
                log_dict['tag'] = tag_tag.text

            # author details
            author_tag = logentry.find('author')
            log_dict['author'] = author_tag.text
            author_attrs = dict(author_tag.attrs)
            log_dict['author_email'] = author_attrs['email']

            # commit date
            date_tag = logentry.find('date')
            log_dict['date'] = mercurial_date_to_datetime(date_tag.text)

            # commit message
            message_tag = logentry.find('msg')
            log_dict['message'] = message_tag.text

            # paths
            paths = []
            paths_tag = logentry.find('paths')
            for path in paths_tag.findAll('path'):
                path_dict = dict(path.attrs)
                path_dict['path'] = path.text
                paths.append(path_dict)
            log_dict['paths'] = paths
            self.log_data.append(log_dict)

    def __iter__(self):
        for item in self.log_data:
            yield item


def get_log(model_reference, revision=None):
    repo_path = model_reference.path
    os.chdir(repo_path)
    cmd_list = [settings.HG_CMD, 'log', '--style=xml']
    if revision:
        cmd_list.append('--rev=%s' % revision)
    xml = subprocess.check_output(cmd_list)
    log_data = MercurialLogData(xml)
    return log_data


def get_latest_revision(model_reference):
    repo_path = model_reference.path
    os.chdir(repo_path)
    # assumes repo is always updated to tip
    revision = subprocess.check_output([settings.HG_CMD, 'id', '-i'])
    revision = revision.strip()
    return revision
