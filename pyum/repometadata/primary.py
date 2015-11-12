from xml.etree import ElementTree
from pyum.repometadata import Data
from pyum.rpm import Rpm

__author__ = 'drews'


class PrimaryData(Data):
    packages = {}
    def _parse(self, param):
        doc = ElementTree.fromstring(param)
        packages = doc.findall("./{0}package".format(self.xmlns))
        for package in packages:
            rpm = Rpm(RepoUrl='')
            rpm._parse_xml(package)
            self.packages[rpm.name] = rpm


class PrimaryDbData(PrimaryData): pass
