from sys import path
path.append("../../../") # Habilita a importação dos arquivo que etão em src/*

import unittest
from services.crawler import Crawler
from services.GameReview.getReviewTotalAmount import getReviewTotalAmount

class TestGetReviewTotalAmount(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.crawler = Crawler()
        self.soup    = self.crawler.reqUrl("https://store.steampowered.com/app/391540/Undertale/")

    def test_getReviewTotalAmount(self):
        """ Verifica se o método getReviewTotalAmount() está funcionando 
        corretamente.

        """

        summary = getReviewTotalAmount(self.soup)

        self.assertIsNotNone(summary)
        self.assertIsInstance(summary, list)
        self.assertGreaterEqual(len(summary), 0)
        self.assertLessEqual(len(summary), 2)

if __name__ == "__main__":
    unittest.main()