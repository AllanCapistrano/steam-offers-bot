from sys import path
path.append("../../../") # Habilita a importação dos arquivo que etão em src/*

import unittest
from services.crawler import Crawler
from services.TabContent.getTabContentNames import getTabContentNames

class TestGetTabContentNames(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        currency     = "us"
        language     = "english"
        category     = "NewReleases"
        self.crawler = Crawler()
        self.soup    = self.crawler.reqUrl(f"https://store.steampowered.com/specials?cc={currency}#p=0&l={language}&tab={category}")

    def test_getTabContentNames(self):
        """ Verifica se o método getTabContentNames() está funcionando 
        corretamente.

        """

        names = getTabContentNames(self.soup)

        self.assertIsNotNone(names)
        self.assertIsInstance(names, list)
        self.assertGreaterEqual(len(names), 0)

if __name__ == "__main__":
    unittest.main()