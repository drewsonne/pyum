__author__ = 'drews'


class Data(object):
    xmlns = '{http://linux.duke.edu/metadata/common}'
    xmlns_rpm = '{http://linux.duke.edu/metadata/rpm}'

    def __init__(self, **kwargs):
        self._attributes = kwargs
        self.repo_url = None

    def __getitem__(self, item):
        if item not in self._attributes:
            raise KeyError("Could not find '{0}'".format(item))
        else:
            return self._attributes[item]

    def setRepoUrl(self, new_url):
        self.repo_url = new_url

    def location(self):
        return "{0}/{1}".format(self.repo_url, self._attributes['location'])

    def _parse(self, xml):
        raise Exception("_parse() is not implemented.")
