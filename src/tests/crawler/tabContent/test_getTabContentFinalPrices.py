from sys import path
path.append("../../../") # Habilita a importação dos arquivo que etão em src/*

import unittest
from services.crawler import Crawler
from services.TabContent.getTabContentFinalPrices import getTabContentFinalPrices

class TestGetTabContentFinalPrices(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        currency     = "us"
        language     = "english"
        category     = "NewReleases"
        self.crawler = Crawler()
        self.soup    = self.crawler.reqUrl(f"https://store.steampowered.com/specials?cc={currency}#p=0&l={language}&tab={category}")

    def test_getTabContentFinalPrices(self):
        """ Verifica se o método getTabContentFinalPrices() está funcionando 
        corretamente.

        """

        finalPrices = getTabContentFinalPrices(self.soup)

        self.assertIsNotNone(finalPrices)
        self.assertIsInstance(finalPrices, list)
        self.assertGreaterEqual(len(finalPrices), 0)

if __name__ == "__main__":
    unittest.main()