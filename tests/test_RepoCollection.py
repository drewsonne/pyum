import types
from unittest import TestCase

import pkg_resources

from pyum.repo import RepoCollection


class TestRepoCollection(TestCase):
    def test_repo_file_loading(self):
        repo_collection = RepoCollection(pkg_resources.resource_filename(__name__, 'resources'))
        self.assertEqual(type(repo_collection.repositories), types.GeneratorType)
        self.assertListEqual(dict(repo_collection.repositories).keys(), [
            'red-hat-enterprise-linux-scalable-file-system-for-rhel-6-entitlement-rpms',
            'red-hat-enterprise-linux-scalable-file-system-for-rhel-6-entitlement-debug-rpms',
            'red-hat-enterprise-linux-scalable-file-system-for-rhel-6-entitlement-source-rpms',
            'updates',
            'base',
            'centosplus',
            'extras'
        ])