from sys import path
path.append("../../") # Habilita a importação dos arquivo que etão em src/*

import unittest
from unittest.mock import patch
from services.crawler import Crawler

class TestGetGameDescription(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.crawler = Crawler()
        self.soup    = self.crawler.reqUrl("https://store.steampowered.com/app/391540/Undertale/")

    def test_getGameDescription(self):
        """ Verifica se o método getGameDescription() está funcionando 
        corretamente.

        """

        description = self.crawler.getGameDescription(self.soup)

        self.assertIsNotNone(description)
        self.assertIsInstance(description, str)

    @patch('bs4.BeautifulSoup', **{'return_value.raiseError.side_effect': Exception()})
    def test_getGameDescription_exception(self, mockedObjectConstructor):
        """ Verifica se o método getGameDescription() está capturando 
        corretamente a exceção.

        """

        mockedSoup = mockedObjectConstructor.return_value.raiseError.side_effect
        ret        = self.crawler.getGameDescription(mockedSoup)
        
        self.assertIsNone(ret)

if __name__ == "__main__":
    unittest.main()