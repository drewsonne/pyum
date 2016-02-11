from pyum.httpclient import HTTPClient

__author__ = 'drews'


class DataParser(object):
    xmlns = '{http://linux.duke.edu/metadata/common}'
    xmlns_rpm = '{http://linux.duke.edu/metadata/rpm}'


class Data(HTTPClient):
    """
    Represents the common attributes of all database types within a yum repository
    """

    def __init__(self, **kwargs):
        """
        Ingest all attributes
        :param kwargs:
        :return:
        """
        self._attributes = kwargs
        self.repo_url = None

    def __getitem__(self, item):
        """
        Forward attribute requests to self._attributes, or try to get them normally.
        :param item:
        :return:
        """
        if item not in self._attributes:
            raise KeyError("Could not find '{0}'".format(item))
        else:
            return self._attributes[item]

    def setRepoUrl(self, new_url):
        """
        Setter function for the repo URL
        :param new_url:
        :return:
        """
        self.repo_url = new_url

    def location(self):
        """
        Predefined format for the location. This should be an @property
        :return:
        """
        return "{0}/{1}".format(self.repo_url.replace('repodata/repomd.xml', ''), self._attributes['location'])

    def load(self):
        """
        Load the repo database from the remote source, and then parse it.
        :return:
        """
        data = self.http_request(self.location())
        self._parse(data)
        return self
