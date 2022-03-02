from sys import path
path.append("../../../") # Habilita a importação dos arquivo que etão em src/*

import unittest
from services.crawler import Crawler
from services.RecommendationByPriceRange.getRecommendationByPriceRangeOriginalPrices import getRecommendationByPriceRangeOriginalPrices

class TestGetRecommendationByPriceRangeOriginalPrices(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        url           = "https://store.steampowered.com/search/?"
        currency      = "us"
        maxPrice      = "50"
        self.language = "english"
        self.crawler  = Crawler()
        self.soup     = self.crawler.reqUrl(f"{url}l={self.language}&maxprice={maxPrice}&cc={currency}")

    def test_getRecommendationByPriceRangeOriginalPrices(self):
        """ Verifica se o método getRecommendationByPriceRangeOriginalPrices() 
        está funcionando corretamente.

        """

        originalPrices = getRecommendationByPriceRangeOriginalPrices(
            soup     = self.soup, 
            language = self.language
        )

        self.assertIsNotNone(originalPrices)
        self.assertIsInstance(originalPrices, list)
        self.assertGreaterEqual(len(originalPrices), 0)

if __name__ == "__main__":
    unittest.main()