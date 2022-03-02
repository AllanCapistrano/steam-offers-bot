from sys import path
path.append("../../../") # Habilita a importação dos arquivo que etão em src/*

import unittest
from services.crawler import Crawler
from services.SpecificGame.getSpecificGameImage import getSpecificGameImage

class TestGetSpecificGameImage(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        currency     = "br"
        gameName     = "Undertale"
        language     = "brazilian"
        self.crawler = Crawler()
        self.soup    = self.crawler.reqUrl(f"https://store.steampowered.com/search/?cc={currency}&l={language}&term={gameName}")

    def test_getSpecificGameImage(self):
        """ Verifica se o método getSpecificGameImage() está funcionando 
        corretamente.

        """

        image = getSpecificGameImage(soup=self.soup)

        self.assertIsNotNone(image)
        self.assertIsInstance(image, str)

if __name__ == "__main__":
    unittest.main()