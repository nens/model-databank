import subprocess
import os
import lxml
from lxml import etree, objectify
import json
from cStringIO import StringIO

from model_databank.conf import settings


class ObjectJSONEncoder(json.JSONEncoder):
    """A specialized JSON encoder that can handle simple lxml objectify types
       >>> from lxml import objectify
       >>> obj = objectify.fromstring("<Book><price>1.50</price><author>W. Shakespeare</author></Book>")
       >>> objectJSONEncoder().encode(obj)
       '{"price": 1.5, "author": "W. Shakespeare"}'
    """
    def default(self,o):
        if isinstance(o, lxml.objectify.IntElement):
            return int(o)
        if isinstance(o, lxml.objectify.NumberElement) or \
           isinstance(o, lxml.objectify.FloatElement):
            return float(o)
        if isinstance(o, lxml.objectify.ObjectifiedDataElement):
            return str(o)
        if hasattr(o, '__dict__'):
            #For objects with a __dict__, return the encoding of the __dict__
            return o.__dict__
        return json.JSONEncoder.default(self, o)


def xml_log_entry_to_json(xml):
    obj = objectify.fromstring(xml)
    return ObjectJSONEncoder().encode(obj)


def get_log(model_reference, style='xml'):
    repo_path = model_reference.path
    os.chdir(repo_path)
#    output = subprocess.check_output([settings.HG_CMD, 'log', '--verbose',
#                                      '--style=%s' % style])
    output = subprocess.check_output([settings.HG_CMD, 'nlog'])
#    if style == 'xml':
#        tree = etree.parse(StringIO(output))
#        output = xml_log_entry_to_json(output)
    return output


def get_latest_revision(model_reference):
    repo_path = model_reference.path
    os.chdir(repo_path)
    # assumes repo is always updated to tip
    revision = subprocess.check_output([settings.HG_CMD, 'id', '-i'])
    revision = revision.strip()
    return revision
