from sys import path
path.append("../../../") # Habilita a importação dos arquivo que etão em src/*

import unittest
from services.crawler import Crawler
from services.TabContent.getTabContentHasPrice import getTabContentHasPrice

class TestGetTabContentHasPrice(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        currency     = "us"
        language     = "english"
        category     = "NewReleases"
        self.crawler = Crawler()
        self.soup    = self.crawler.reqUrl(f"https://store.steampowered.com/specials?cc={currency}#p=0&l={language}&tab={category}")

    def test_getTabContentHasPrice(self):
        """ Verifica se o método getTabContentHasPrice() está funcionando 
        corretamente.

        """

        (hasPrice, gameWithOutPrice) = getTabContentHasPrice(self.soup)

        self.assertIsNotNone(hasPrice)
        self.assertIsNotNone(gameWithOutPrice)
        self.assertIsInstance(hasPrice, list)
        self.assertIsInstance(gameWithOutPrice, bool)
        self.assertGreaterEqual(len(hasPrice), 0)

if __name__ == "__main__":
    unittest.main()