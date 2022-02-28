from sys import path
path.append("../../../") # Habilita a importação dos arquivo que etão em src/*

import unittest
from services.crawler import Crawler
from services.TabContent.getTabContentImages import getTabContentImages

class TestGetTabContentImages(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        currency     = "us"
        language     = "english"
        category     = "NewReleases"
        self.crawler = Crawler()
        self.soup    = self.crawler.reqUrl(f"https://store.steampowered.com/specials?cc={currency}#p=0&l={language}&tab={category}")

    def test_getTabContentImages(self):
        """ Verifica se o método getTabContentImages() está funcionando 
        corretamente.

        """

        images = getTabContentImages(self.soup)

        self.assertIsNotNone(images)
        self.assertIsInstance(images, list)
        self.assertGreaterEqual(len(images), 0)

if __name__ == "__main__":
    unittest.main()