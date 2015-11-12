from xml.etree import ElementTree
from pyum.repometadata.BaseData import Data

__author__ = 'drews'


class GroupData(Data):
    groups = []

    def _parse(self, param):
        doc = ElementTree.fromstring(param)
        groups = doc.findall("./{0}group".format(self.xmlns))
        pass