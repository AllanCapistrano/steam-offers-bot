from sys import path
path.append("../../../") # Habilita a importação dos arquivo que etão em src/*

import unittest
from services.crawler import Crawler
from services.RecommendationByPriceRange.getRecommendationByPriceRangeUrls import getRecommendationByPriceRangeUrls

class TestGetRecommendationByPriceRangeUrls(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        url           = "https://store.steampowered.com/search/?"
        currency      = "us"
        maxPrice      = "50"
        self.language = "english"
        self.crawler  = Crawler()
        self.soup     = self.crawler.reqUrl(f"{url}l={self.language}&maxprice={maxPrice}&cc={currency}")

    def test_getRecommendationByPriceRangeUrls(self):
        """ Verifica se o método getRecommendationByPriceRangeUrls() está 
        funcionando corretamente.

        """

        urls = getRecommendationByPriceRangeUrls(soup=self.soup)

        self.assertIsNotNone(urls)
        self.assertIsInstance(urls, list)
        self.assertGreaterEqual(len(urls), 0)

if __name__ == "__main__":
    unittest.main()