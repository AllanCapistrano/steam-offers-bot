from sys import path
path.append("../../../") # Habilita a importação dos arquivo que etão em src/*

import unittest
from unittest.mock import patch
from services.crawler import Crawler
from services.SpecificGame.getSpecificGameOriginalPrice import getSpecificGameOriginalPrice

class TestGetSpecificGameOriginalPrice(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        currency          = "us"
        gameName          = "Undertale"
        self.language     = "english"
        self.crawler      = Crawler()
        self.soup         = self.crawler.reqUrl(f"https://store.steampowered.com/search/?cc={currency}&l={self.language}&term={gameName}")
        game              = self.soup.find(id='search_resultsRows').find(class_='search_result_row ds_collapse_flag')
        self.haveDiscount = True if len(game.find(class_='search_price').contents) > 1 else False

    def test_getSpecificGameOriginalPrice(self):
        """ Verifica se o método getSpecificGameOriginalPrice() está funcionando 
        corretamente.

        """

        originalPrice = getSpecificGameOriginalPrice(soup=self.soup, haveDiscount=self.haveDiscount, language=self.language)

        self.assertIsNotNone(originalPrice)
        self.assertIsInstance(originalPrice, str)
        self.assertEqual(originalPrice, "$9.99")

    @patch('bs4.BeautifulSoup', **{'return_value.raiseError.side_effect': Exception()})
    def test_getSpecificGameOriginalPrice_exception(self, mockedObjectConstructor):
        """ Verifica se o método getSpecificGameOriginalPrice() está capturando 
        corretamente a exceção.

        """

        mockedSoup = mockedObjectConstructor.return_value.raiseError.side_effect
        ret        = getSpecificGameOriginalPrice(soup=mockedSoup, haveDiscount=self.haveDiscount, language=self.language)
        
        self.assertIsNotNone(ret)
        self.assertIsInstance(ret, str)

if __name__ == "__main__":
    unittest.main()