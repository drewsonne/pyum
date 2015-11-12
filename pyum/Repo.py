from configparser import RawConfigParser
from pyum.HTTPClient import HTTPClient
from pyum.repometadata import RepoMetadata

__author__ = 'drews'


class RepoFile(RawConfigParser):
    def __init__(self, path_to_config):
        super(RepoFile, self).__init__()
        self.path_to_config = path_to_config
        self.read(self.path_to_config)
        self.yum_variables = {}

    def __getattribute__(self, item):
        if item == 'keys':
            sections = self.sections()
            return sections
        else:
            return super(RepoFile, self).__getattribute__(item)

    def __getitem__(self, key):
        if key != self.default_section and not self.has_section(key):
            raise KeyError(key)
        return Repo.from_section(self._proxies[key], self.yum_variables)

    def set_yum_variables(self, **kwargs):
        self.yum_variables = kwargs


class Repo(HTTPClient):
    @classmethod
    def from_section(cls, section, yum_variables):
        repo = Repo(**dict(section))
        repo.set_yum_variables(**yum_variables)
        return repo

    def __init__(self, **kwargs):
        self.repo_params = kwargs
        self.yum_variables = {}

    def __getattr__(self, key):
        if key not in self.repo_params:
            return super(Repo, self).__getattribute__(key)
        else:
            return self.render_string(self.repo_params[key])

    def render_string(self, string):
        for key, value in self.yum_variables.items():
            string = string.replace('$' + key, value)
        return string

    def set_yum_variables(self, **kwargs):
        self.yum_variables = kwargs

    def _parse_repo_data(self):
        mirrorlist = self._get_mirrorlist()
        for mirror in mirrorlist:
            if self._url_is_reachable(mirror):
                break
        return RepoMetadata(mirror)

    def _get_mirrorlist(self):
        if self._url_is_reachable(self.mirrorlist):
            return self._http_request(self.mirrorlist).decode('utf-8').split("\n")
        else:
            raise ConnectionError('Could not connect to \'{0}\''.format(self.mirrorlist))


class EtcRepos(object): pass
