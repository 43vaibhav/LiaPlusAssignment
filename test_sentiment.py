import unittest
from chatbot import SentimentAnalyzer

class TestSentiment(unittest.TestCase):
    def test_positive(self):
        a = SentimentAnalyzer()
        label, score = a.analyze("I love this!")
        self.assertEqual(label, "Positive")
        self.assertGreater(score, 0.5)

    def test_negative(self):
        a = SentimentAnalyzer()
        label, score = a.analyze("This sucks.")
        self.assertEqual(label, "Negative")
        self.assertLess(score, -0.3)

    def test_trend(self):
        a = SentimentAnalyzer()
        a.analyze("bad")
        a.analyze("great")
        trend = a.get_trend_summary()
        self.assertIn("Shifts", trend)

if __name__ == '__main__':
    unittest.main(verbosity=2)