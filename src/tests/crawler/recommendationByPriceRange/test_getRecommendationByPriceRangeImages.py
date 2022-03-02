from sys import path
path.append("../../../") # Habilita a importação dos arquivo que etão em src/*

import unittest
from services.crawler import Crawler
from services.RecommendationByPriceRange.getRecommendationByPriceRangeImages import getRecommendationByPriceRangeImages

class TestGetRecommendationByPriceRangeImages(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        url           = "https://store.steampowered.com/search/?"
        currency      = "us"
        maxPrice      = "50"
        self.language = "english"
        self.crawler  = Crawler()
        self.soup     = self.crawler.reqUrl(f"{url}l={self.language}&maxprice={maxPrice}&cc={currency}")

    def test_getRecommendationByPriceRangeImages(self):
        """ Verifica se o método getRecommendationByPriceRangeImages() está 
        funcionando corretamente.

        """

        images = getRecommendationByPriceRangeImages(soup=self.soup)

        self.assertIsNotNone(images)
        self.assertIsInstance(images, list)
        self.assertGreaterEqual(len(images), 0)

if __name__ == "__main__":
    unittest.main()