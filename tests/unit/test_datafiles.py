import unittest
import os
import unittest.mock as mock

from pyDataBank import DataFiles


class TestDataFiles(unittest.TestCase):

    def test_pack(self):
        settings = {
            'files': {
                'parent': 'tests/unit/resources/folder1',
                'depth': -1,
                'caseSensitive': True,
                'definitions': {
                    'file': r'fiLe'
                }
            },
            'fileset': {
                'parent': 'tests/unit/resources/folder1',
                'depth': 0,
                'caseSensitive': False,
                'definitions': {
                    'set': r'.*'
                }
            },
            'mykey1' : 'value1',
            'mykey2' : [1, 2]
        }

        resources = DataFiles(settings)
        datapack = resources.generatePack()

        filedict = datapack.getFileDict()
        filedictvalues = [os.path.basename(file) for file in filedict.values()]
        self.assertCountEqual(filedict.keys(), ['file'])
        self.assertCountEqual(filedictvalues, ['fiLe2_1.txt'])

        filesetdict = datapack.getFilesetDict()
        filesetdictvalues = [os.path.basename(
            file) for files in filesetdict.values() for file in files]
        self.assertCountEqual(filesetdictvalues, [
                              'file1_1.txt', 'file1_2.txt'])

        filelist = datapack.getFileList()
        files = [os.path.basename(file) for file in filelist]
        self.assertCountEqual(files, ['fiLe2_1.txt',
                                      'file1_1.txt', 'file1_2.txt'])

        others = datapack.getOthers()
        self.assertEqual(others,{'mykey1': 'value1', 'mykey2': [1, 2]})

    @mock.patch("pyDataBank.DataFiles._openDialog")
    def test_open_dialog(self, mock_dialog):
        settings = {
            'dialogs': {
                'images': {
                    'tip': 'select images',
                    'type': ['png', 'jpg']
                },
                'txt': {
                    'tip': 'provide txt file',
                    'type': 'txt',
                    'set': False
                }
            }
        }

        images = ['image1.jpg', 'image2.png']
        txt = 'doc.txt'

        mock_dialog.side_effect = [images, txt]
        resources = DataFiles(settings)

        files = resources.datapack.getFileDict()
        filesets = resources.datapack.getFilesetDict()
        filelist = resources.datapack.getFileList()

        self.assertCountEqual(files.keys(), ['txt'])
        self.assertCountEqual(files.values(), [txt])

        self.assertCountEqual(filesets.keys(), ['images'])
        self.assertCountEqual(filesets.values(), [images])

        self.assertCountEqual(
            filelist, ['image1.jpg', 'image2.png', 'doc.txt'])
