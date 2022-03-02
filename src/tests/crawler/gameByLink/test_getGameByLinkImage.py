from sys import path
path.append("../../../") # Habilita a importação dos arquivo que etão em src/*

import unittest
from services.crawler import Crawler
from services.GameByLink.getGameByLinkImage import getGameByLinkImage

class TestGetGameByLinkImage(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.crawler    = Crawler()
    
    def test_getGameByLinkImage(self):
        """ Verifica se o método getGameByLinkImage() está funcionando 
        corretamente.

        """

        soup  = self.crawler.reqUrl("https://store.steampowered.com/app/391540/Undertale/")
        image = getGameByLinkImage(soup)

        self.assertIsNotNone(image)
        self.assertIsInstance(image, str)

    def test_getGameByLinkImage_invalid_url(self):
        """ Verifica se o método getGameByLinkImage() com uma URL inválida está 
        funcionando corretamente.

        """

        soup  = self.crawler.reqUrl("https://store.steampowered.com/app/000000/InvalidGame/")
        image = getGameByLinkImage(soup)

        self.assertIsNone(image)

if __name__ == "__main__":
    unittest.main()