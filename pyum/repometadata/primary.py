import datetime

import bitmath
from pyum import rpm

from pyum.repometadata import Data
from pyum.repometadata.base import DataParser
from pyum.rpm import RpmParser

__author__ = 'drews'


class PrimaryDataParser(DataParser):
    STATE_PARSING = 'null'
    STATE_PARSING_PACKAGE = 'parsing_package'
    STATE_PARSING_FORMAT = 'parsing_format'
    STATE_PARSING_PROVIDES = 'parsing_provides'
    STATE_PARSING_REQUIRES = 'parsing_requires'
    STATE_PARSING_CONFLICTS = 'parsing_conflicts'
    STATE_PARSING_OBSOLETES = 'parsing_obsoletes'

    def __init__(self):
        self._state = self.STATE_PARSING
        self._tag = None
        self._package = None
        self._primary_data = PrimaryData()
        self._files = []
        self._parse_lookup = {
            'checksum': self._parse_checksum,
            'metadata': self._parse_metadata,
            'package': self._parse_package,
            'version': self._parse_version,
            'format': self._parse_format,
            'time': self._parse_time,
            'size': self._parse_size,
            'entry': self._parse_entry,
            'provides': self._parse_provides,
            'requires': self._parse_requires,
            'conflicts': self._parse_conflicts,
            'obsoletes': self._parse_obsoletes,
            'file': self._parse_file,
            'description': self._parse_default,
            'packager': self._parse_default,
            'location': self._parse_default,
            'summary': self._parse_default,
            'arch': self._parse_default,
            'name': self._parse_default,
            'url': self._parse_default,
            'license': self._parse_default,
            'vendor': self._parse_default,
            'group': self._parse_default,
            'buildhost': self._parse_default,
            'sourcerpm': self._parse_default,
            'header-range': self._parse_default
        }

    def start(self, tag, attribute):
        tag = tag.replace(self.xmlns, '').replace(self.xmlns_rpm, '')
        self._tag = tag
        self._parse_lookup[tag](tag, attribute)

    def end(self, raw_tag):
        tag = raw_tag.replace(self.xmlns, '').replace(self.xmlns_rpm, '')
        if tag in ['name', 'arch', 'version', 'checksum', 'summary', 'description', 'packager', 'url', 'time', 'size',
                   'location']:
            return
        elif tag in ['license', 'vendor', 'group', 'buildhost', 'sourcerpm', 'header-range']:
            return
        elif tag == 'entry':
            return
        elif tag in ['provides', 'requires', 'conflicts', 'obsoletes']:
            setattr(self._format, tag, getattr(self, '_' + tag))
            setattr(self, '_' + tag, [])
            self._state = self.STATE_PARSING_FORMAT
        elif tag == 'file':
            return
        elif tag == 'format':
            self._package.format = self._format
        elif tag == 'package':
            self._primary_data.append_package(self._package)
            self._package = None
        elif tag == 'metadata':
            return
        else:
            self._package

        return

    def data(self, data):
        data = data.strip()
        if (not data) or (self._state == self.STATE_PARSING):
            return
        elif self._state == self.STATE_PARSING_PACKAGE:
            setattr(self._package, self._tag, data)
        elif self._state == self.STATE_PARSING_FORMAT:
            setattr(self._format, self._tag, data)
        else:
            asdh = "help"
        return

    def close(self):
        return self._primary_data

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

    def _parse_provides(self, tag, attributes):
        self._state = self.STATE_PARSING_PROVIDES
        self._provides = []

    def _parse_requires(self, tag, attributes):
        self._state = self.STATE_PARSING_REQUIRES
        self._requires = []

    def _parse_conflicts(self, tag, attributes):
        self._state = self.STATE_PARSING_CONFLICTS
        self._conflicts = []

    def _parse_obsoletes(self, tag, attributes):
        self._state = self.STATE_PARSING_OBSOLETES
        self._obsoletes = []

    def _parse_entry(self, tag, attributes):
        if self._state == self.STATE_PARSING_PROVIDES:
            self._provides.append(DependencyEntry(tag, **attributes))
        elif self._state == self.STATE_PARSING_REQUIRES:
            self._requires.append(DependencyEntry(tag, **attributes))
        elif self._state == self.STATE_PARSING_CONFLICTS:
            self._conflicts.append(DependencyEntry(tag, **attributes))
        elif self._state == self.STATE_PARSING_OBSOLETES:
            self._obsoletes.append(DependencyEntry(tag, **attributes))

    def _parse_file(self, tag, attributes):
        self._files.append(File(**attributes))


class File(object):
    def __init__(self, **kwargs):
        self.attributes = kwargs


class DependencyEntry(object):
    def __init__(self, tag, **kwargs):
        self.tag = tag
        self.attributes = kwargs

    def is_library(self):
        return not self.is_package()

    def is_package(self):
        return ('epoch' in self.attributes) or \
               ('version' in self.attributes) or \
               ('rel' in self.attributes)


class PrimaryData(Data):
    xml_parse = PrimaryDataParser

    def __init__(self, **kwargs):
        super(PrimaryData, self).__init__(**kwargs)
        self._packages = []

    @property
    def packages(self):
        for package in self._packages:
            yield package.name, package

    def append_package(self, new_package):
        self._packages.append(new_package)

    def find_rpms(self, packages_names):
        packages = []
        for package_name in packages_names:
            if package_name in self.packages:
                packages.append(self.packages[package_name])
        return packages


class PrimaryDbData(PrimaryData): pass
