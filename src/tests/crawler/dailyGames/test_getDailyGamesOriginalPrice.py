from sys import path
path.append("../../../") # Habilita a importação dos arquivo que etão em src/*

import unittest
from services.crawler import Crawler
from services.DailyGames.getDailyGamesOriginalPrice import getDailyGamesOriginalPrice

class TestGetDailyGamesOriginalPrice(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.crawler = Crawler()

    def test_getDailyGamesOriginalPrice_brazilian_portuguese(self):
        """ Verifica se o método getDailyGamesOriginalPrice() em português 
        brasileiro está funcionando corretamente.

        """
        
        currency = "br"
        language = "brazilian"
        url      = f"https://store.steampowered.com/specials?cc={currency}&l={language}"
        soup     = self.crawler.reqUrl(url)

        originalPrices = getDailyGamesOriginalPrice(soup=soup, language=language)

        self.assertIsInstance(originalPrices, list)
        self.assertGreaterEqual(len(originalPrices), 0)

    def test_getDailyGamesOriginalPrice_english(self):
        """ Verifica se o método getDailyGamesOriginalPrice() em inglês está 
        funcionando corretamente.

        """
        
        currency = "us"
        language = "english"
        url      = f"https://store.steampowered.com/specials?cc={currency}&l={language}"
        soup     = self.crawler.reqUrl(url)

        originalPrices = getDailyGamesOriginalPrice(soup=soup, language=language)

        self.assertIsInstance(originalPrices, list)
        self.assertGreaterEqual(len(originalPrices), 0)

if __name__ == "__main__":
    unittest.main()