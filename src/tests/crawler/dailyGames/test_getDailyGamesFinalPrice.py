from sys import path
path.append("../../../") # Habilita a importação dos arquivo que etão em src/*

import unittest
from services.crawler import Crawler
from services.DailyGames.getDailyGamesFinalPrice import getDailyGamesFinalPrice

class TestGetDailyGamesFinalPrice(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.crawler = Crawler()
        
    def test_getDailyGamesFinalPrice_brazilian_portuguese(self):
        """ Verifica se o método getDailyGamesFinalPrice() em português 
        brasileiro está funcionando corretamente.

        """
        
        currency = "br"
        language = "brazilian"
        url      = f"https://store.steampowered.com/specials?cc={currency}&l={language}"
        soup     = self.crawler.reqUrl(url)

        finalPrices = getDailyGamesFinalPrice(soup=soup, language=language)

        self.assertIsInstance(finalPrices, list)
        self.assertGreaterEqual(len(finalPrices), 0)

    def test_getDailyGamesFinalPrice_english(self):
        """ Verifica se o método getDailyGamesFinalPrice() em inglês está 
        funcionando corretamente.

        """
        
        currency = "us"
        language = "english"
        url      = f"https://store.steampowered.com/specials?cc={currency}&l={language}"
        soup     = self.crawler.reqUrl(url)

        finalPrices = getDailyGamesFinalPrice(soup=soup, language=language)

        self.assertIsInstance(finalPrices, list)
        self.assertGreaterEqual(len(finalPrices), 0)

if __name__ == "__main__":
    unittest.main()