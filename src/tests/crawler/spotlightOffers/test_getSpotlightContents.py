from sys import path
path.append("../../../") # Habilita a importação dos arquivo que etão em src/*

import unittest
from services.crawler import Crawler
from services.SpotlightOffers.getSpotlightContents import getSpotlightContents

class TestGetSpotlightContents(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.crawler = Crawler()
        self.soup    = self.crawler.reqUrl("https://store.steampowered.com/specials?cc=br&l=english")

    def test_getSpotlightContents(self):
        """ Verifica se o método getSpotlightContents() está funcionando 
        corretamente.

        """

        contents = getSpotlightContents(self.soup)

        self.assertIsNotNone(contents)
        self.assertIsInstance(contents, list)

if __name__ == "__main__":
    unittest.main()