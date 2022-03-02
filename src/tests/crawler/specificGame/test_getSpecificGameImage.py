from sys import path
path.append("../../../") # Habilita a importação dos arquivo que etão em src/*

import unittest
from unittest.mock import patch
from services.crawler import Crawler
from services.SpecificGame.getSpecificGameImage import getSpecificGameImage

class TestGetSpecificGameImage(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        currency     = "us"
        gameName     = "Undertale"
        language     = "english"
        self.crawler = Crawler()
        soup         = self.crawler.reqUrl(f"https://store.steampowered.com/search/?cc={currency}&l={language}&term={gameName}")
        self.game    = soup.find(id='search_resultsRows').find(class_='search_result_row ds_collapse_flag')

    def test_getSpecificGameImage(self):
        """ Verifica se o método getSpecificGameImage() está funcionando 
        corretamente.

        """

        image = getSpecificGameImage(soup=self.game)

        self.assertIsNotNone(image)
        self.assertIsInstance(image, str)

    @patch('bs4.BeautifulSoup', **{'return_value.raiseError.side_effect': Exception()})
    def test_getSpecificGameImage_exception(self, mockedObjectConstructor):
        """ Verifica se o método getSpecificGameImage() está capturando 
        corretamente a exceção.

        """

        mockedSoup = mockedObjectConstructor.return_value.raiseError.side_effect
        ret        = getSpecificGameImage(soup=mockedSoup)
        
        self.assertIsNone(ret)

if __name__ == "__main__":
    unittest.main()