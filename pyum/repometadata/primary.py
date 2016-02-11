import datetime

import bitmath
from lxml import etree
from pyum import rpm

from pyum.repometadata import Data
from pyum.repometadata.base import DataParser
from pyum.rpm import RpmParser

__author__ = 'drews'


class PrimaryData(Data):
    packages = {}

    def _parse(self, xml_path):
        parser = etree.XMLParser(target=PrimaryDataParser())
        results = etree.parse(xml_path, parser)
        doc = ElementTree.fromstring(param)
        packages = doc.findall("./{0}package".format(self.xmlns))
        for package in packages:
            rpm = RpmParser.load(package)
            rpm.repo_url = self.repo_url.replace('repodata/repomd.xml', '')
            self.packages[rpm.name] = rpm

    def find_rpms(self, packages_names):
        packages = []
        for package_name in packages_names:
            if package_name in self.packages:
                packages.append(self.packages[package_name])
        return packages


class PrimaryDbData(PrimaryData): pass


class PrimaryDataParser(DataParser):
    STATE_PARSING = 0
    STATE_PARSING_PACKAGE = 1
    STATE_PARSING_FORMAT = 2

    def __init__(self):
        self._state = self.STATE_PARSING
        self._tag = None
        self._package = None
        self._primary_data = PrimaryData()
        self._parse_lookup = {
            'checksum': self._parse_checksum,
            'metadata': self._parse_metadata,
            'package': self._parse_package,
            'version': self._parse_version,
            'format': self._parse_format,
            'time': self._parse_time,
            'size': self._parse_size,
            'description': self._parse_default,
            'packager': self._parse_default,
            'location': self._parse_default,
            'summary': self._parse_default,
            'arch': self._parse_default,
            'name': self._parse_default,
            'url': self._parse_default
        }

    def start(self, tag, attribute):
        tag = tag.replace(self.xmlns, '').replace(self.xmlns_rpm, '')
        self._tag = tag
        self._parse_lookup[tag](tag, attribute)

    def end(self, tag):
        tag = tag.replace(self.xmlns, '')
        if tag == 'package':
            tag

    def data(self, data):
        data = data.strip()
        if (not data) or (self._state == self.STATE_PARSING):
            return
        elif self._state == self.STATE_PARSING_PACKAGE:
            setattr(self._package, self._tag, data)
        else:
            asdh = "help"
        return

    def close(self):
        return self.primary_data

    def _parse_format(self, tag, attributes):
        self._state = self.STATE_PARSING_FORMAT
        self._format = rpm.Format()

    def _parse_size(self, tag, attributes):
        self._package.size = {
            'archive': bitmath.Byte(int(attributes['archive'])),
            'installed': bitmath.Byte(int(attributes['installed'])),
            'package': bitmath.Byte(int(attributes['package']))
        }

    def _parse_time(self, tag, attributes):
        self._package.time = {
            'build': datetime.datetime.fromtimestamp(int(attributes['build'])),
            'file': datetime.datetime.fromtimestamp(int(attributes['file']))
        }

    def _parse_checksum(self, tag, attributes):
        self._package.checksum = {
            'type': attributes['type'],
            'pkgid': True if attributes['pkgid'] == 'YES' else False
        }

    def _parse_version(self, tag, attributes):
        self._package.epoch = attributes['epoch']
        self._package.version = attributes['ver']
        self._package.release = attributes['rel']

    def _parse_default(self, tag, attributes):
        pass

    def _parse_package(self, tag, attributes):
        self._state = self.STATE_PARSING_PACKAGE
        self._package = rpm.Package()

    def _parse_metadata(self, tag, attributes):
        self._primary_data.num_packages = attributes['packages']
