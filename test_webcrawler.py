import unittest
from unittest.mock import patch
from webcrawler import WebCrawler

class TestWebCrawler(unittest.TestCase):
    def setUp(self):
        self.crawler = WebCrawler()




        

    def test_crawl(self):
        # Mocking requests.get method to avoid actual HTTP requests
        with patch('requests.get') as mocked_get:
            mocked_get.return_value.ok = True
            mocked_get.return_value.text = """
                <html>
                    <head><title>Test Page</title></head>
                    <body>
                        <a href="http://example.com/page1">Page 1</a>
                        <a href="http://example.com/page2">Page 2</a>
                    </body>
                </html>
            """
            self.crawler.crawl("http://example.com")

        self.assertIn("http://example.com", self.crawler.index)
        self.assertEqual(len(self.crawler.index), 3)  # Index should contain base URL and two links
        self.assertEqual(len(self.crawler.visited), 3)  # Including base URL and two links
        self.assertEqual(self.crawler.links_found, 2)

    def test_max_depth_reached(self):
        # Test case to ensure crawling stops when maximum depth is reached
        with patch('requests.get') as mocked_get:
            mocked_get.return_value.ok = True
            mocked_get.return_value.text = """
                <html>
                    <head><title>Test Page</title></head>
                    <body>
                        <a href="http://example.com/page1">Page 1</a>
                    </body>
                </html>
            """
            self.crawler.crawl("http://example.com", max_depth=0)

        self.assertEqual(self.crawler.links_found, 0)  # No links found because max depth is 0
        self.assertEqual(len(self.crawler.visited), 0)  # Only base URL visited

    def test_error_handling(self):
        # Mocking requests.get method to simulate request exception
        with patch('requests.get') as mocked_get:
            mocked_get.side_effect = Exception("Mocked exception")
            self.crawler.crawl("http://invalidurl.com")

        self.assertNotIn("http://invalidurl.com", self.crawler.index)
        self.assertEqual(len(self.crawler.visited), 1)  # Only base URL visited
        self.assertEqual(self.crawler.links_found, 0)

    def test_duplicate_links(self):
        # Test case to ensure duplicate links are not crawled multiple times
        with patch('requests.get') as mocked_get:
            mocked_get.return_value.ok = True
            mocked_get.return_value.text = """
                <html>
                    <head><title>Test Page</title></head>
                    <body>
                        <a href="http://example.com/page1">Page 1</a>
                        <a href="http://example.com/page1">Page 1 (Duplicate)</a>
                    </body>
                </html>
            """
            self.crawler.crawl("http://example.com")

        self.assertEqual(self.crawler.links_found, 1)  # Only one unique link found
        self.assertEqual(len(self.crawler.visited), 2)  # Including base URL and one link

    
if __name__ == '__main__':
    unittest.main()
