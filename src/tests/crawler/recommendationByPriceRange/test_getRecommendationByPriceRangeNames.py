from sys import path
path.append("../../../") # Habilita a importação dos arquivo que etão em src/*

import unittest
from services.crawler import Crawler
from services.RecommendationByPriceRange.getRecommendationByPriceRangeNames import getRecommendationByPriceRangeNames

class TestGetRecommendationByPriceRangeNames(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        url           = "https://store.steampowered.com/search/?"
        currency      = "us"
        maxPrice      = "50"
        self.language = "english"
        self.crawler  = Crawler()
        self.soup     = self.crawler.reqUrl(f"{url}l={self.language}&maxprice={maxPrice}&cc={currency}")

    def test_getRecommendationByPriceRangeNames(self):
        """ Verifica se o método getRecommendationByPriceRangeNames() está 
        funcionando corretamente.

        """

        names = getRecommendationByPriceRangeNames(soup=self.soup)

        self.assertIsNotNone(names)
        self.assertIsInstance(names, list)
        self.assertGreaterEqual(len(names), 0)

if __name__ == "__main__":
    unittest.main()