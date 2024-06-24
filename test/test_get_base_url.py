import unittest
from unittest.mock import MagicMock, patch
from youtube_dl.downloader.f4m import get_base_url, branch_coverage
from youtube_dl.utils import xpath_text

class TestGetBaseURL(unittest.TestCase):
    def setUp(self):
        branch_coverage.update({
            "get_base_url_1": False,
            "get_base_url_2": False
        })
        self.manifest = MagicMock()

    @patch('youtube_dl.downloader.f4m.xpath_text', return_value='http://example.com/base/')
    def test_get_base_url_with_baseURL(self, mock_xpath_text):
        result = get_base_url(self.manifest)
        self.assertEqual(result, 'http://example.com/base/')
        self.assertTrue(branch_coverage["get_base_url_1"])
        self.assertFalse(branch_coverage["get_base_url_2"])

    @patch('youtube_dl.downloader.f4m.xpath_text', return_value=None)
    def test_get_base_url_without_baseURL(self, mock_xpath_text):
        result = get_base_url(self.manifest)
        self.assertIsNone(result)
        self.assertFalse(branch_coverage["get_base_url_1"])
        self.assertTrue(branch_coverage["get_base_url_2"])

if __name__ == '__main__':
    unittest.main()
