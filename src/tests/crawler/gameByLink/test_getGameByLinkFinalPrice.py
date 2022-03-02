from sys import path
path.append("../../../") # Habilita a importação dos arquivo que etão em src/*

import unittest
from unittest.mock import patch
from services.crawler import Crawler
from services.GameByLink.getGameByLinkFinalPrice import getGameByLinkFinalPrice

class TestGetGameByLinkFinalPrice(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.crawler    = Crawler()
        self.language   = "english" 

    def test_getGameByLinkFinalPrice(self):
        """ Verifica se o método getGameByLinkFinalPrice() está funcionando 
        corretamente.

        """

        soup       = self.crawler.reqUrl("https://store.steampowered.com/app/391540/Undertale/")
        finalPrice = getGameByLinkFinalPrice(soup=soup, language=self.language)

        self.assertIsNotNone(finalPrice)
        self.assertIsInstance(finalPrice, str)
    
    def test_getGameByLinkFinalPrice_invalid_url(self):
        """ Verifica se o método getGameByLinkFinalPrice() com uma URL inválida
        está funcionando corretamente.

        """

        soup       = self.crawler.reqUrl("https://google.com")
        finalPrice = getGameByLinkFinalPrice(soup=soup, language=self.language)

        self.assertEqual(finalPrice, "Not available!")

    @patch('bs4.BeautifulSoup', **{'return_value.raiseError.side_effect': Exception()})
    def test_getGameByLinkFinalPrice_exception(self, mockedObjectConstructor):
        """ Verifica se o método getGameByLinkFinalPrice() está capturando 
        corretamente a exceção.

        """

        mockedSoup = mockedObjectConstructor.return_value.raiseError.side_effect
        ret        = getGameByLinkFinalPrice(soup=mockedSoup, language=self.language)
        
        self.assertIsNotNone(ret)
        self.assertIsInstance(ret, str)

if __name__ == "__main__":
    unittest.main()