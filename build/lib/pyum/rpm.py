__author__ = 'drews'


class Rpm(object):
    xmlns = '{http://linux.duke.edu/metadata/common}'
    xmlns_rpm = '{http://linux.duke.edu/metadata/rpm}'

    def package(self, package_name):
        return Package.from_url(self.find_package(Name=package_name))

    def _parse_xml(self, xml):
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
        pass

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