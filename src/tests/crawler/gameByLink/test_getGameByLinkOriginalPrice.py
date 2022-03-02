from sys import path
path.append("../../../") # Habilita a importação dos arquivo que etão em src/*

import unittest
from unittest.mock import patch
from services.crawler import Crawler
from services.GameByLink.getGameByLinkOriginalPrice import getGameByLinkOriginalPrice

class TestGetGameByLinkOriginalPrice(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.crawler    = Crawler()
        self.language   = "english" 

    def test_getGameByLinkOriginalPrice(self):
        """ Verifica se o método getGameByLinkOriginalPrice() está funcionando 
        corretamente.

        """

        soup       = self.crawler.reqUrl("https://store.steampowered.com/app/391540/Undertale/")
        original = getGameByLinkOriginalPrice(soup=soup, language=self.language)

        self.assertIsNotNone(original)
        self.assertIsInstance(original, str)
    
    def test_getGameByLinkOriginalPrice_invalid_url(self):
        """ Verifica se o método getGameByLinkOriginalPrice() com uma URL inválida
        está funcionando corretamente.

        """

        soup       = self.crawler.reqUrl("https://google.com")
        original = getGameByLinkOriginalPrice(soup=soup, language=self.language)

        self.assertEqual(original, "Not available!")

    @patch('bs4.BeautifulSoup', **{'return_value.raiseError.side_effect': Exception()})
    def test_getGameByLinkOriginalPrice_exception(self, mockedObjectConstructor):
        """ Verifica se o método getGameByLinkOriginalPrice() está capturando 
        corretamente a exceção.

        """

        mockedSoup = mockedObjectConstructor.return_value.raiseError.side_effect
        ret        = getGameByLinkOriginalPrice(soup=mockedSoup, language=self.language)
        
        self.assertIsNotNone(ret)
        self.assertIsInstance(ret, str)

if __name__ == "__main__":
    unittest.main()