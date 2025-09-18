import unittest
from omni.core.crawler import GoogleNewsCrawler

class TestGoogleNewsCrawler(unittest.TestCase):
    def test_construct_url_with_filters(self):
        crawler = GoogleNewsCrawler()
        urls = crawler._construct_url_with_filters(search="economy", time_period="1d", financial_flag=False)
        self.assertIsInstance(urls, list)
        self.assertTrue(len(urls) > 0)
        self.assertTrue(all("news.google.com" in url for url in urls))

if __name__ == "__main__":
    unittest.main()
