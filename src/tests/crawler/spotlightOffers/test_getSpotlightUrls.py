from sys import path
path.append("../../../") # Habilita a importação dos arquivo que etão em src/*

import unittest
from services.crawler import Crawler
from services.SpotlightOffers.getSpotlightUrls import getSpotlightUrls

class TestGetSpotlightUrls(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.crawler = Crawler()
        self.soup    = self.crawler.reqUrl("https://store.steampowered.com/specials?cc=br&l=english")

    def test_getSpotlightUrls(self):
        """ Verifica se o método getSpotlightUrls() está funcionando 
        corretamente.

        """

        urls = getSpotlightUrls(self.soup)

        self.assertIsNotNone(urls)
        self.assertIsInstance(urls, list)

if __name__ == "__main__":
    unittest.main()