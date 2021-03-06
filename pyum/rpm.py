# import yum
import tempfile
from xml import etree

from pyrpm.rpm import RPM
from pyum.httpclient import HTTPClient

__author__ = 'drews'


class RpmParser(object):
    @staticmethod
    def load(fp):
        """

        :param fp:
        :return Rpm:
        """
        parser = etree.XMLParser(target=RpmParser())
        return etree.parse(fp.read(), parser)

    def __init__(self):
        self.rpm = Rpm()


class Rpm(object):
    """
    Represents the xml structure defining where to find a the specific version of an RPM.
    """
    xmlns = '{http://linux.duke.edu/metadata/common}'
    xmlns_rpm = '{http://linux.duke.edu/metadata/rpm}'

    @property
    def package(self):
        """
        Return the package from a URL
        :return:
        """
        return Package.from_url(self.uri())

    def uri(self):
        return '{0}/{1}'.format(self.repo_url, self.location)

    def parse_xml(self, xml):
        self.name = xml.find('.//{xmlns}name'.format(xmlns=self.xmlns)).text
        self.arch = xml.find('.//{xmlns}arch'.format(xmlns=self.xmlns)).text
        self.version = xml.find('.//{xmlns}version'.format(xmlns=self.xmlns)).attrib['ver']
        self.release = xml.find('.//{xmlns}version'.format(xmlns=self.xmlns)).attrib['rel']

        checksum_element = xml.find('.//{xmlns}checksum'.format(xmlns=self.xmlns))
        self.checksum_type = checksum_element.attrib['type']
        self.checksum = checksum_element.text

        self.summary = xml.find('.//{xmlns}summary'.format(xmlns=self.xmlns)).text
        self.description = xml.find('.//{xmlns}description'.format(xmlns=self.xmlns)).text
        self.packager = xml.find('.//{xmlns}packager'.format(xmlns=self.xmlns)).text
        self.url = xml.find('.//{xmlns}url'.format(xmlns=self.xmlns)).text

        self.build_time = xml.find('.//{xmlns}time'.format(xmlns=self.xmlns)).attrib['build']
        self.file_time = xml.find('.//{xmlns}time'.format(xmlns=self.xmlns)).attrib['file']

        size_element = xml.find('.//{xmlns}size'.format(xmlns=self.xmlns)).attrib
        self.installed_size = size_element['installed']
        self.package_size = size_element['package']
        self.archive_size = size_element['archive']

        self.location = xml.find('.//{xmlns}location'.format(xmlns=self.xmlns)).attrib['href']

        self._parse_xml_format(xml.find('.//{xmlns}format'.format(xmlns=self.xmlns)))

    def _parse_xml_format(self, xml):
        self.license = xml.find('.//{xmlns}license'.format(xmlns=self.xmlns_rpm)).text
        self.vendor = xml.find('.//{xmlns}vendor'.format(xmlns=self.xmlns_rpm)).text
        self.group = xml.find('.//{xmlns}group'.format(xmlns=self.xmlns_rpm)).text
        self.buildhost = xml.find('.//{xmlns}buildhost'.format(xmlns=self.xmlns_rpm)).text
        self.sourcerpm = xml.find('.//{xmlns}sourcerpm'.format(xmlns=self.xmlns_rpm)).text

        self.provides = []
        provides_entries = xml.findall('.//{xmlns}provides/{xmlns}entry'.format(xmlns=self.xmlns_rpm))
        for entry in provides_entries:
            if 'flags' not in entry.attrib:
                self.provides.append(entry.attrib['name'])

        self.requires = []
        requires_entries = xml.findall('.//{xmlns}requires/{xmlns}entry'.format(xmlns=self.xmlns_rpm))
        for entry in requires_entries:
            if 'flags' not in entry.attrib:
                self.requires.append(entry.attrib['name'])


class Format(object):
    pass


class Package(object):
    """
    Represents the XML description of an RPM in a repomd xml database.
    """

    @staticmethod
    def from_url(url):
        """
        Given a URL, return a package
        :param url:
        :return:
        """
        package_data = HTTPClient().http_request(url=url, decode=None)
        return Package(raw_data=package_data)

    MODE_RAW_DATA = 0
    MODE_FILE_PATH = 1

    def __init__(self, raw_data=None):
        self.mode = None
        if raw_data is not None:
            self.data = raw_data
            self.mode = self.MODE_RAW_DATA
            self.fp = tempfile.NamedTemporaryFile()
            self.fp.write(raw_data)
            self.fp.seek(0)
            self.rpm = RPM.load(self.fp)

    def __enter__(self):
        return self

    def dependencies(self):
        """
        Read the contents of the rpm itself
        :return:
        """
        cpio = self.rpm.gzip_file.read()
        content = cpio.read()
        return []

    # yb = yum.YumBase()

    def __exit__(self, *excinfo):
        """
        Make sure we close the file after we finish the 'with'
        :param excinfo:
        :return:
        """
        self.rpm.__exit__(*excinfo)
        if self.mode == self.MODE_RAW_DATA:
            self.fp.close()
