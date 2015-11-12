from unittest import TestCase
import pkg_resources
import pyum

__author__ = 'drews'


class TestRepo(TestCase):
    def test_load_from_config(self):
        repos = pyum.RepoFile(pkg_resources.resource_filename(__name__, 'resources/test_repo.repo'))
        repos.set_yum_variables(
            releasever='7',
            basearch='x86_64'
        )

        self.assertEqual(repos.keys, [
            "red-hat-enterprise-linux-scalable-file-system-for-rhel-6-entitlement-rpms",
            "red-hat-enterprise-linux-scalable-file-system-for-rhel-6-entitlement-source-rpms",
            "red-hat-enterprise-linux-scalable-file-system-for-rhel-6-entitlement-debug-rpms"
        ])

        self.assertIsInstance(repos['red-hat-enterprise-linux-scalable-file-system-for-rhel-6-entitlement-rpms'],
                              pyum.Repo)
        self.assertIsInstance(repos['red-hat-enterprise-linux-scalable-file-system-for-rhel-6-entitlement-source-rpms'],
                              pyum.Repo)
        self.assertIsInstance(repos['red-hat-enterprise-linux-scalable-file-system-for-rhel-6-entitlement-debug-rpms'],
                              pyum.Repo)

        # Test the base rpms repo.
        rpms_content = {
            "name": "Red Hat Enterprise Linux Scalable File System (for RHEL 6 Entitlement) (RPMs)",
            "baseurl": "https://cdn.redhat.com/content/dist/rhel/entitlement-6/releases/7/x86_64/scalablefilesystem/os",
            "enabled": "1",
            "gpgcheck": "1",
            "gpgkey": "file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release",
            "sslverify": "1",
            "sslcacert": "/etc/rhsm/ca/redhat-uep.pem",
            "sslclientkey": "/etc/pki/entitlement/key.pem",
            "sslclientcert": "/etc/pki/entitlement/11300387955690106.pem"
        }

        rpms_repo = repos['red-hat-enterprise-linux-scalable-file-system-for-rhel-6-entitlement-rpms']
        for key, value in rpms_content.items():
            self.assertEqual(getattr(rpms_repo, key), value, "{0} does not contain '{1}'".format(rpms_repo, key))

        # Test the source rpms repo
        source_rpms_content = {
            "name": "Red Hat Enterprise Linux Scalable File System (for RHEL 6 Entitlement) (Source RPMs)",
            "baseurl": "https://cdn.redhat.com/content/dist/rhel/entitlement-6/releases/7/x86_64/scalablefilesystem/source/SRPMS",
            "enabled": "0",
            "gpgcheck": "1",
            "gpgkey": "file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release",
            "sslverify": "1",
            "sslcacert": "/etc/rhsm/ca/redhat-uep.pem",
            "sslclientkey": "/etc/pki/entitlement/key.pem",
            "sslclientcert": "/etc/pki/entitlement/11300387955690106.pem"
        }

        source_repo = repos['red-hat-enterprise-linux-scalable-file-system-for-rhel-6-entitlement-source-rpms']
        for key, value in source_rpms_content.items():
            self.assertTrue(hasattr(source_repo, key))
            self.assertEqual(getattr(source_repo, key), value)

        # Test the debug rpms repo
        debug_rpms_content = {
            "name": "Red Hat Enterprise Linux Scalable File System (for RHEL 6 Entitlement) (Debug RPMs)",
            "baseurl": "https://cdn.redhat.com/content/dist/rhel/entitlement-6/releases/7/x86_64/scalablefilesystem/debug",
            "enabled": "0",
            "gpgcheck": "1",
            "gpgkey": "file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release",
            "sslverify": "1",
            "sslcacert": "/etc/rhsm/ca/redhat-uep.pem",
            "sslclientkey": "/etc/pki/entitlement/key.pem",
            "sslclientcert": "/etc/pki/entitlement/11300387955690106.pem"
        }

        debug_repo = repos['red-hat-enterprise-linux-scalable-file-system-for-rhel-6-entitlement-debug-rpms']
        for key, value in debug_rpms_content.items():
            self.assertTrue(hasattr(debug_repo, key))
            self.assertEqual(getattr(debug_repo, key), value)
