from pyum.HTTPClient import HTTPClient
from xml.etree import ElementTree
from pyum.repometadata.BaseData import Data
from pyum.repometadata.group import GroupData
from pyum.repometadata.primary import PrimaryDbData, PrimaryData

__author__ = 'drews'


class RepoMetadata(HTTPClient):
    def __init__(self, repo_path, xmlns='http://linux.duke.edu/metadata/repo'):
        self.repo_url = repo_path
        self.xmlns = xmlns

        self._attributes = {}

    def load(self):
        xml = self._get_repo_data()
        self._parse_remomd(xml)

    def _get_repo_data(self):
        repomd = "{0}/repodata/repomd.xml".format(self.repo_url)
        if self._url_is_reachable(repomd):
            return self._http_request(repomd).decode('utf-8')
        else:
            raise ConnectionError("Could not reach repo '{0}'".format(self.repo_url))

    def _parse_remomd(self, repo_metadata):
        doc = ElementTree.fromstring(repo_metadata)
        ns = doc.attrib
        xmlns = "{{{0}}}".format(self.xmlns)
        data_elements = doc.findall("./{0}data".format(xmlns))
        if len(data_elements) > 0:
            for data_element in data_elements:
                attributes = {}
                for child in data_element.findall(".//*"):
                    value = child.text
                    attribute = child.tag.replace(xmlns, "")
                    if attribute.endswith('checksum'):
                        attribute = "{0}-{1}".format(attribute, child.get('type'))
                    elif child.tag == '{0}location'.format(xmlns):
                        value = child.get('href')
                    attributes[attribute] = value
                new_data = self._dataType(data_element.get('type'))(**attributes)
                new_data.setRepoUrl(self.repo_url)
                self._attributes[data_element.get('type')] = new_data

    def groups(self):
        return self._attributes['group']

    def _dataType(self, data_type):
        return {
            'group': GroupData,
            'filelists': FilelistData,
            'group_gz': GroupGzData,
            'primary': PrimaryData,
            'primary_db': PrimaryDbData,
            'other_db': OtherDbData,
            'other': OtherData,
            'filelists_db': FileListDbData
        }[data_type]

class GroupGzData(GroupData): pass


class FilelistData(Data): pass


class FileListDbData(FilelistData): pass


class OtherDbData(Data): pass


class OtherData(OtherDbData): pass

