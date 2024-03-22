import unittest  # Import the unittest module to create and run tests
from ranker import Ranker  # Import the Ranker class to be tested


class TestRanker(unittest.TestCase):  # Define a test case class for the Ranker, inheriting from unittest.TestCase

    def setUp(self):  # setUp method is called before each test method
        self.ranker = Ranker()  # Create an instance of Ranker to be used in the test methods

    def test_rank_results(self):  # Test method to verify rank_results function works as expected
        # Setup a sample index and results to use for testing
        index = {
            "example.com": "Python programming tutorials and guides.",
            "example.net": "Advanced Python programming and development.",
            "example.org": "Introduction to programming with Python."
        }
        results = list(index.keys())  # Convert index keys to a list to represent URLs to be ranked
        keyword = "programming"  # Define a keyword to search and rank the results by

        # Expected ranking order based on the occurrence of the keyword
        expected_rank_order = ["example.com", "example.net", "example.org"]

        ranked_results = self.ranker.rank_results(results, index, keyword)  # Call the rank_results method
        ranked_urls = list(ranked_results.keys())  # Extract the URLs from the ranked results in their ranked order

        self.assertEqual(ranked_urls, expected_rank_order)  # Assert that the actual ranking matches the expected ranking

    def test_rank_results_with_no_keyword_match(self):  # Test method for when the keyword doesn't match any text
        # Setup a sample index where the keyword doesn't match any text
        index = {
            "example.com": "Python tutorials.",
            "example.net": "Python development."
        }
        results = list(index.keys())  # Convert index keys to a list of URLs
        keyword = "java"  # Define a keyword that doesn't match any text in the index

        ranked_results = self.ranker.rank_results(results, index, keyword)  # Call the rank_results method

        # Assert that all URLs are returned and have a score of 0 since the keyword doesn't match
        self.assertEqual(len(ranked_results), len(results))  # Check if all URLs are included
        for url in results:
            self.assertIn(url, ranked_results)  # Ensure each URL is in the ranked results
            self.assertEqual(ranked_results[url], 0)  # Verify that the score for each URL is 0

    def test_rank_results_case_insensitivity(self):  # Test method to ensure ranking is case-insensitive
        # Setup a sample index with mixed case text
        index = {
            "example.com": "Python Programming Tutorials."
        }
        results = ["example.com"]  # List of URLs to rank
        keyword = "programming"  # Define a keyword with different case

        ranked_results = self.ranker.rank_results(results, index, keyword)  # Call the rank_results method

        # Assert that the keyword count is 1, demonstrating case-insensitive matching
        self.assertEqual(ranked_results["example.com"], 1)


if __name__ == '__main__':
    unittest.main()  # Run the tests if the script is executed directly
