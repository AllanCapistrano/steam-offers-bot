from sys import path
path.append("../../../") # Habilita a importação dos arquivo que etão em src/*

import unittest
from services.crawler import Crawler
from services.TabContent.getTabContentOriginalPrices import getTabContentOriginalPrices

class TestGetTabContentOriginalPrices(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        currency     = "us"
        language     = "english"
        category     = "NewReleases"
        self.crawler = Crawler()
        self.soup    = self.crawler.reqUrl(f"https://store.steampowered.com/specials?cc={currency}#p=0&l={language}&tab={category}")

    def test_getTabContentOriginalPrices(self):
        """ Verifica se o método getTabContentOriginalPrices() está funcionando 
        corretamente.

        """

        originalPrices = getTabContentOriginalPrices(self.soup)

        self.assertIsNotNone(originalPrices)
        self.assertIsInstance(originalPrices, list)
        self.assertGreaterEqual(len(originalPrices), 0)

if __name__ == "__main__":
    unittest.main()