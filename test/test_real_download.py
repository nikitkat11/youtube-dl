import sys
print(sys.path)
import unittest
from unittest.mock import patch, MagicMock
from youtube_dl.downloader.dash import DashSegmentsFD, branch_coverage

class TestDashFDRealDownload(unittest.TestCase):

    def setUp(self):
        self.dash_fd = DashSegmentsFD()

    @patch('youtube_dl.downloader.dash.DashSegmentsFD._download_fragment')
    @patch('youtube_dl.downloader.dash.DashSegmentsFD._finish_frag_download')
    def test_real_download(self, mock_finish, mock_download):
        info_dict = {
            'is_live': False,
            'fragments': [{'url': 'http://example.com/frag1'}, {'url': 'http://example.com/frag2'}]
        }
        mock_download.return_value = True
        result = self.dash_fd.real_download('testfile', info_dict)
        self.assertTrue(result)
        self.assertTrue(branch_coverage["real_download_2"])
        self.assertTrue(branch_coverage["real_download_3"])
        self.assertFalse(branch_coverage["real_download_1"])
        self.assertFalse(branch_coverage["real_download_4"])
        mock_finish.assert_called_once()

if __name__ == '__main__':
    unittest.main()