from configparser import RawConfigParser
from pyum.httpclient import HTTPClient
from pyum.repometadata import RepoMetadata

__author__ = 'drews'


class RepoFile(RawConfigParser, object):
    """
    Represents a file on disk, describing one or more repositories in /etc/yum.repods.d/*.repo
    """

    def __init__(self, path_to_config):
        """
        Path on disk to the ini file containing the repo description
        :param path_to_config str:
        :return:
        """
        super(RepoFile, self).__init__()
        self.path_to_config = path_to_config
        self.read(self.path_to_config)
        self.yum_variables = {}

    def __getattr__(self, item):
        if item == 'keys':
            sections = self.sections()
            return sections
        else:
            return super(RepoFile, self).__getattribute__(item)

    def __getitem__(self, key):
        if not self.has_section(key):
            raise KeyError(key)
        return Repo.from_section(self.items(key), self.yum_variables)

    def set_yum_variables(self, releasever, basearch):
        """
        Variables which are usually injected from an OS level.
        :param releasever int: OS major version
        :param basearch string: One of either 'i386' or 'x86_64'.
        :return:
        """
        self.yum_variables = {
            'releasever': str(releasever),
            'basearch': basearch
        }


class Repo(HTTPClient):
    """
    Represents a single repository
    """

    @staticmethod
    def from_section(section, yum_variables):
        repo = Repo(**dict(section))
        repo.set_yum_variables(**yum_variables)
        return repo

    def __init__(self, **kwargs):
        self.repo_params = kwargs
        self.yum_variables = {}
        enabled_state = self.repo_params.get('enabled', False)
        if enabled_state in ['0', '1']:
            enabled_state = (False if enabled_state == '0' else True)
        self.repo_params['enabled'] = enabled_state

    def __getattr__(self, key):
        if key not in self.repo_params:
            return super(Repo, self).__getattribute__(key)
        else:
            return self.render_string(self.repo_params[key])

    @property
    def enabled(self):
        return ('1' if self.__getattr__('enabled') else '0')

    def render_string(self, string):
        if isinstance(string, str):
            for key, value in self.yum_variables.items():
                string = string.replace('$' + key, value)
        return string

    def set_yum_variables(self, releasever, basearch):
        """
        Variables which are usually injected from an OS level.
        :param releasever int: OS major version
        :param basearch string: One of either 'i386' or 'x86_64'.
        :return:
        """
        self.yum_variables = {
            'releasever': str(releasever),
            'basearch': basearch
        }

    def primary(self):
        return self._parse_repo_data().load().primary()

    def _parse_repo_data(self):
        if 'baseurl' in self.repo_params:
            return RepoMetadata(self.repo_params['baseurl'])
        else:
            mirrorlist = self._get_mirrorlist()
            for mirror in mirrorlist:
                if not mirror.endswith('repodata/repomd.xml'):
                    mirror = mirror + 'repodata/repomd.xml'
                if self._url_is_reachable(mirror):
                    break
            return RepoMetadata(mirror)

    def _get_mirrorlist(self):
        if self._url_is_reachable(self.mirrorlist):
            mirrorlist = self.http_request(self.mirrorlist).decode('utf-8')
        else:
            raise HTTPClient.ConnectionError('Could not connect to \'{0}\''.format(self.mirrorlist))
        if mirrorlist.startswith("<?xml"):
            return self.parse_xml_mirrorlist(mirrorlist)
        else:
            return mirrorlist.split("\n")

    @staticmethod
    def parse_xml_mirrorlist(xml):
        mirrorlist = []
        doc = ElementTree.fromstring(xml)
        urls = doc.findall(
                './/{http://www.metalinker.org/}files/{http://www.metalinker.org/}file/{http://www.metalinker.org/}resources/{http://www.metalinker.org/}url')
        for url in urls:
            if ('type' in url.attrib) and (url.attrib['type'] in ['http', 'https']):
                mirrorlist.append(url.text)
        return mirrorlist
