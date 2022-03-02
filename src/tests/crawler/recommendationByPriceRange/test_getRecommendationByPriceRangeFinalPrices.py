from sys import path
path.append("../../../") # Habilita a importação dos arquivo que etão em src/*

import unittest
from services.crawler import Crawler
from services.RecommendationByPriceRange.getRecommendationByPriceRangeFinalPrices import getRecommendationByPriceRangeFinalPrices

class TestGetRecommendationByPriceRangeFinalPrices(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        url           = "https://store.steampowered.com/search/?"
        currency      = "us"
        maxPrice      = "50"
        self.language = "english"
        self.crawler  = Crawler()
        self.soup     = self.crawler.reqUrl(f"{url}l={self.language}&maxprice={maxPrice}&cc={currency}")

    def test_getRecommendationByPriceRangeFinalPrices(self):
        """ Verifica se o método getRecommendationByPriceRangeFinalPrices() está 
        funcionando corretamente.

        """

        finalPrices = getRecommendationByPriceRangeFinalPrices(
            soup     = self.soup, 
            language = self.language
        )

        self.assertIsNotNone(finalPrices)
        self.assertIsInstance(finalPrices, list)
        self.assertGreaterEqual(len(finalPrices), 0)

if __name__ == "__main__":
    unittest.main()