import os
from unittest import TestCase
import pkg_resources
from pyum.repometadata import RepoMetadata, PrimaryData
__author__ = 'drews'


class TestRepoMetadata(TestCase):
    def test_group_listing(self):
        primary = PrimaryData(test=None)
        primary.setRepoUrl(os.path.realpath(pkg_resources.resource_filename(__name__, 'resources')))
        primary._parse(pkg_resources.resource_string(__name__, 'resources/primary.xml').decode('utf-8'))

    def test_url_resolution(self):
        md = RepoMetadata('http://example.com/yum')
        md._parse_remomd(pkg_resources.resource_string(__name__, 'resources/repomd.xml'))

        self.assertEqual(md.groups().location(),
                         'http://example.com/yum/repodata/175ddec2056ec6b5ef267cea35f8ec679314afbfb019957e53f71725bcc5d829-c7-x86_64-comps.xml')

    def test_load_from_config(self):
        md = RepoMetadata('dummy_path')
        md._parse_remomd(pkg_resources.resource_string(__name__, 'resources/repomd.xml'))

        group = md._attributes['group']
        self.assertEqual(group['checksum-sha256'], '175ddec2056ec6b5ef267cea35f8ec679314afbfb019957e53f71725bcc5d829')
        self.assertEqual(group['location'],
                         'repodata/175ddec2056ec6b5ef267cea35f8ec679314afbfb019957e53f71725bcc5d829-c7-x86_64-comps.xml')
        self.assertEqual(group['timestamp'], '1427842246')
        self.assertEqual(group['size'], '741067')

        filelists = md._attributes['filelists']
        self.assertEqual(filelists['checksum-sha256'],
                         '453d04f8ea01148c074d54308dc4003ee0e3914e2d9387b8e305ade3f6dce294')
        self.assertEqual(filelists['open-checksum-sha256'],
                         'c4677d30aa1c8384d81eb8517a7567dbc9223964f55904e675dcadd456a298f2')
        self.assertEqual(filelists['location'],
                         'repodata/453d04f8ea01148c074d54308dc4003ee0e3914e2d9387b8e305ade3f6dce294-filelists.xml.gz')
        self.assertEqual(filelists['timestamp'], '1427842225')
        self.assertEqual(filelists['size'], '6180591')
        self.assertEqual(filelists['open-size'], '85822689')

        group_gz = md._attributes['group_gz']
        self.assertEqual(group_gz['checksum-sha256'],
                         '0e6e90965f55146ba5025ea450f822d1bb0267d0299ef64dd4365825e6bad995')
        self.assertEqual(group_gz['open-checksum-sha256'],
                         '175ddec2056ec6b5ef267cea35f8ec679314afbfb019957e53f71725bcc5d829')
        self.assertEqual(group_gz['location'],
                         'repodata/0e6e90965f55146ba5025ea450f822d1bb0267d0299ef64dd4365825e6bad995-c7-x86_64-comps.xml.gz')
        self.assertEqual(group_gz['timestamp'], '1427842246')
        self.assertEqual(group_gz['size'], '157580')

        primary = md._attributes['primary']
        self.assertEqual(primary['checksum-sha256'], '1386c5af55bda40669bb5ed91e0a22796c3ed7325367506109b09ea2657f22bd')
        self.assertEqual(primary['open-checksum-sha256'],
                         '03473500623f4a5c73e21fca97b9dedecd5a93f05b8bb891cf14638839fb29c3')
        self.assertEqual(primary['location'],
                         'repodata/1386c5af55bda40669bb5ed91e0a22796c3ed7325367506109b09ea2657f22bd-primary.xml.gz')
        self.assertEqual(primary['timestamp'], '1427842225')
        self.assertEqual(primary['size'], '2528031')
        self.assertEqual(primary['open-size'], '23175717')

        primary_db = md._attributes['primary_db']
        self.assertEqual(primary_db['checksum-sha256'],
                         '9c92f78fb6f22491ea7414f5a844ad08c604139b151d4c702f2c0d6ae092c86f')
        self.assertEqual(primary_db['open-checksum-sha256'],
                         '76d5e8b221e082f926b184a996280e1aa829c59c5e8fa718d64f046476f7778c')
        self.assertEqual(primary_db['location'],
                         'repodata/9c92f78fb6f22491ea7414f5a844ad08c604139b151d4c702f2c0d6ae092c86f-primary.sqlite.bz2')
        self.assertEqual(primary_db['timestamp'], '1427842246')
        self.assertEqual(primary_db['database_version'], '10')
        self.assertEqual(primary_db['size'], '5319521')
        self.assertEqual(primary_db['open-size'], '25624576')

        other_db = md._attributes['other_db']
        self.assertEqual(other_db['checksum-sha256'],
                         '1ea314ec7e4d7168bf16e67799237a42fd2b9857fdb0f18a7ea923d2fb22ebe4')
        self.assertEqual(other_db['open-checksum-sha256'],
                         '185310ed7cc7377f075b376dcb81be3024d436a54ca41908c3ecba4d43fb61a3')
        self.assertEqual(other_db['location'],
                         'repodata/1ea314ec7e4d7168bf16e67799237a42fd2b9857fdb0f18a7ea923d2fb22ebe4-other.sqlite.bz2')
        self.assertEqual(other_db['timestamp'], '1427842230')
        self.assertEqual(other_db['database_version'], '10')
        self.assertEqual(other_db['size'], '2325240')
        self.assertEqual(other_db['open-size'], '15666176')

        other = md._attributes['other']
        self.assertEqual(other['checksum-sha256'], '8d102164ca862a58e99c42583205b4753bf14f473d5528d85bf2f9d8a7b83c31')
        self.assertEqual(other['open-checksum-sha256'],
                         '858cf36199e6124cb1b60d99f4c72935cb89fa976cbf13c3b16f894faaf36631')
        self.assertEqual(other['location'],
                         'repodata/8d102164ca862a58e99c42583205b4753bf14f473d5528d85bf2f9d8a7b83c31-other.xml.gz')
        self.assertEqual(other['timestamp'], '1427842225')
        self.assertEqual(other['size'], '1385777')
        self.assertEqual(other['open-size'], '17092218')

        filelists_db = md._attributes['filelists_db']
        self.assertEqual(filelists_db['checksum-sha256'],
                         '81c0a01775962c10a3e85f2124cdd8d984d72930674c655a4cd2c9c7aa568134')
        self.assertEqual(filelists_db['open-checksum-sha256'],
                         '3f72512693d04cc7cd136d4605baf95da21830f5f691c1416e2e5b79b2b4f89b')
        self.assertEqual(filelists_db['location'],
                         'repodata/81c0a01775962c10a3e85f2124cdd8d984d72930674c655a4cd2c9c7aa568134-filelists.sqlite.bz2')
        self.assertEqual(filelists_db['timestamp'], '1427842240')
        self.assertEqual(filelists_db['database_version'], '10')
        self.assertEqual(filelists_db['size'], '6256795')
        self.assertEqual(filelists_db['open-size'], '39652352')
