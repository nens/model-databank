import os
import logging
import subprocess
from datetime import datetime

from BeautifulSoup import BeautifulSoup as Soup

from model_databank import patch
from model_databank.conf import settings


logger = logging.getLogger(__name__)


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
        root_tag = soup.find('log')
        # Find a right way to parse the diff/patch (if any). root_tag.text
        # returns all the tag texts. Probably best to use a regular
        # expression for this. For example, everything from diff until </log>.
        # USe patch.py for parsing the patch.

        # Sample root_tag:
        # ---------------
        # <log>
        # <logentry revision="1" node="fbbc56677d59ac31477148cb85655d284100a33a">
        # <author email="sander.smits@nelen-schuurmans.nl">Sander Smits</author>
        # <date>2013-03-13T16:43:12+01:00</date>
        # <msg xml:space="preserve">Disable autostart</msg>
        # <paths>
        # <path action="M">Hillegersberg.mdu</path>
        # </paths>
        # </logentry>
        # diff -r 9da59e314661 -r fbbc56677d59 Hillegersberg.mdu
        # --- a/Hillegersberg.mdu	Wed Mar 13 15:55:18 2013 +0100
        # +++ b/Hillegersberg.mdu	Wed Mar 13 16:43:12 2013 +0100
        # @@ -1,7 +1,7 @@
        # # Generated on 16:29:02, 06-02-2013
        #
        # [model]
        # -AutoStart                    = 4                   # 0: NoAutoStart, 1: AutoStart, 2: AutoStartStop
        # +AutoStart                    = 0                   # 0: NoAutoStart, 1: AutoStart, 2: AutoStartStop
        #
        # [geometry]
        # WaterLevelFile               =                     # initial water level file
        #
        # </log>

        self.patch = None
        if root_tag.text:
            # TODO: PM this is not corrent see comment above
            self.patch = root_tag.text
            self.patch = None  # do not set for now

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
            if paths_tag:
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
    repo_path = model_reference.symlink
    os.chdir(repo_path)
    # --verbose is needed to include the paths in the xml log
    cmd_list = [settings.HG_CMD, 'log', '--style=xml', '--verbose']
    if revision:
        cmd_list.append('--rev=%s' % revision)
        cmd_list.append('--patch')
    try:
        xml = subprocess.check_output(cmd_list, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError, error:
        # error has returncode and output fields. output is set, because
        # stderr=subprocess.STDOUT is defined
        if error.output.startswith('abort:'):
            # '--patch' does not work on big files return output like:
            # abort: /home/blabla/mercurial/templates/map-cmdline.xml:
            # no key named '05m_20m_k4_1m.grd@fbac6436ef8a:
            # not found in manifest'
            try:
                # do not include '--patch' this time
                cmd_list = cmd_list[:-1]
                xml = subprocess.check_output(cmd_list,
                                                 stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError, error:
                logger.exception("unknown error: %s" % error.output)
            else:
                return MercurialLogData(xml)
        else:
            logger.exception("unknown error: %s" % error.output)
    else:
        return MercurialLogData(xml)


def get_latest_revision(model_reference):
    repo_path = model_reference.symlink
    os.chdir(repo_path)
    # assumes repo is always updated to tip
    revision = subprocess.check_output([settings.HG_CMD, 'id', '-i'])
    revision = revision.strip()
    return revision


def get_file_tree(model_reference):
    repo_path = model_reference.symlink
    os.chdir(repo_path)
    output = subprocess.check_output([settings.HG_CMD, 'status', '--all'])
    raw_file_tree = output.split('\n')
    # item[2:] removes 'M ' or 'C ' from file or directory name
    file_tree = [item[2:] for item in raw_file_tree]
    return file_tree
