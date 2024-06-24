import sys
print(sys.path)
import unittest
from unittest.mock import patch, MagicMock
from youtube_dl.downloader import get_suitable_downloader, branch_coverage

class TestCommonFunctions(unittest.TestCase):

    @patch('youtube_dl.utils.determine_protocol')
    @patch('youtube_dl.downloader._get_suitable_downloader')
    def test_get_suitable_downloader(self, mock_get_suitable_downloader, mock_determine_protocol):
        mock_determine_protocol.return_value = 'http'
        mock_get_suitable_downloader.return_value = 'suitable_downloader'
        info_dict = {
            'url': 'http://example.com/video',
            'formats': []
        }
        result = get_suitable_downloader(info_dict)
        self.assertEqual(result, 'suitable_downloader')
        self.assertTrue(branch_coverage["get_suitable_downloader_1"])
        self.assertTrue(branch_coverage["get_suitable_downloader_2"])

if __name__ == '__main__':
    unittest.main()
