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
            rpm = Rpm()
            rpm._parse_xml(package)
            rpm.repo_url = self.repo_url.replace('repodata/repomd.xml','')
            self.packages[rpm.name] = rpm

    def find_rpms(self, packages_names):
        packages = []
        for package_name in packages_names:
            if package_name in self.packages:
                packages.append(self.packages[package_name])
        return packages


class PrimaryDbData(PrimaryData): pass
