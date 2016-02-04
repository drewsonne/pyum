from xml.etree import ElementTree
from pyum.repometadata.base import Data

__author__ = 'drews'


class GroupData(Data):
    """
    Represents the XML database describing packages groups in the repository
    """
    groups = []

    def _parse(self, param):
        doc = ElementTree.fromstring(param)
        groups = doc.findall("./{0}group".format(self.xmlns))
        # TODO Pick up coding from here!!
        raise Exception("This is where you stopped coding.")
