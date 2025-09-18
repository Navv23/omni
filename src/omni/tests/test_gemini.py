import unittest
import os
from omni.core.classifier import GeminiClient

class TestGeminiClient(unittest.TestCase):
    def test_prompt_format(self):
        os.environ["GEMINI_API_KEY"] = "dummy"
        client = GeminiClient(model_name="gemini-1.5-flash")
        prompt = client._finance_news_prompt("Test news article")
        self.assertIn("15-Point Digest", prompt)
        self.assertIn("Overall Sentiment", prompt)
        self.assertIn("Stock Recommendations", prompt)

if __name__ == "__main__":
    unittest.main()
