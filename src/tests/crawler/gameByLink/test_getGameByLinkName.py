from sys import path
from unicodedata import name
path.append("../../../") # Habilita a importação dos arquivo que etão em src/*

import unittest
from services.crawler import Crawler
from services.GameByLink.getGameByLinkName import getGameByLinkName

class TestGetGameByLinkName(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.crawler    = Crawler()
    
    def test_getGameByLinkName(self):
        """ Verifica se o método getGameByLinkName() está funcionando 
        corretamente.

        """
        
        soup = self.crawler.reqUrl("https://store.steampowered.com/app/391540/Undertale/")
        name = getGameByLinkName(soup=soup)

        self.assertIsNotNone(name)
        self.assertIsInstance(name, str)

    def test_getGameByLinkName_invalid_url(self):
        """ Verifica se o método getGameByLinkName() com uma URL inválida está 
        funcionando corretamente.

        """

        soup  = self.crawler.reqUrl("https://store.steampowered.com/app/000000/InvalidGame/")
        name = getGameByLinkName(soup)

        self.assertIsNone(name)
        
if __name__ == "__main__":
    unittest.main()