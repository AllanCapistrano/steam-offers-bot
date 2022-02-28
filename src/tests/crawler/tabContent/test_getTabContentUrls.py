from sys import path
path.append("../../../") # Habilita a importação dos arquivo que etão em src/*

import unittest
from services.crawler import Crawler
from services.TabContent.getTabContentUrls import getTabContentUrls

class TestGetTabContentUrls(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        currency     = "us"
        language     = "english"
        category     = "NewReleases"
        self.crawler = Crawler()
        self.soup    = self.crawler.reqUrl(f"https://store.steampowered.com/specials?cc={currency}#p=0&l={language}&tab={category}")

    def test_getTabContentUrls(self):
        """ Verifica se o método getTabContentUrls() está funcionando 
        corretamente.

        """

        urls = getTabContentUrls(self.soup)

        self.assertIsNotNone(urls)
        self.assertIsInstance(urls, list)
        self.assertGreaterEqual(len(urls), 0)

if __name__ == "__main__":
    unittest.main()