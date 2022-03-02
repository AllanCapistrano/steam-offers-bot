from sys import path
path.append("../../../") # Habilita a importação dos arquivo que etão em src/*

import unittest
from services.crawler import Crawler
from services.SpotlightOffers.getSpotlightImages import getSpotlightImages

class TestGetSpotlightImages(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.crawler = Crawler()
        self.soup    = self.crawler.reqUrl("https://store.steampowered.com/specials?cc=br&l=english")

    def test_getSpotlightImages(self):
        """ Verifica se o método getSpotlightImages() está funcionando 
        corretamente.

        """

        images = getSpotlightImages(self.soup)

        self.assertIsNotNone(images)
        self.assertIsInstance(images, list)

if __name__ == "__main__":
    unittest.main()