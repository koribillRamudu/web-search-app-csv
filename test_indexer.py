import unittest
from indexer import Indexer


class TestIndexer(unittest.TestCase):

    def setUp(self):
        self.indexer = Indexer()

    def test_index_page(self):
        # Test indexing a single page
        self.indexer.index_page("example.com", "Example Domain")
        self.assertIn("example.com", self.indexer.index)
        self.assertEqual(self.indexer.index["example.com"], "Example Domain")

        # Test updating an existing page
        self.indexer.index_page("example.com", "Updated Example Domain")
        self.assertEqual(self.indexer.index["example.com"], "Updated Example Domain")

    def test_search_found(self):
        # Setup by indexing some pages
        self.indexer.index_page("example.com", "This is a test")
        self.indexer.index_page("example.net", "Another test page")
        # Search for a keyword that exists
        results = self.indexer.search("test")
        self.assertEqual(len(results), 2)
        self.assertTrue("example.com" in results)
        self.assertTrue("example.net" in results)

    def test_search_not_found(self):
        # Setup by indexing a page
        self.indexer.index_page("example.com", "No relevant keyword here")
        # Search for a keyword that does not exist
        results = self.indexer.search("missing")
        self.assertEqual(len(results), 0)

    def test_search_case_insensitivity(self):
        # Setup by indexing a page
        self.indexer.index_page("example.com", "Mixed CASE Testing")
        # Search should be case insensitive
        results = self.indexer.search("mixed case")
        self.assertEqual(len(results), 1)
        self.assertIn("example.com", results)


if __name__ == '__main__':
    unittest.main()
