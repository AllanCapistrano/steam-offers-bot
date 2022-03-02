from sys import path
path.append("../../../") # Habilita a importação dos arquivo que etão em src/*

import unittest
from services.crawler import Crawler
from services.DailyGames.getDailyGamesUrls import getDailyGamesUrls

class TestGetDailyGamesUrls(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.crawler = Crawler()
        self.soup    = self.crawler.reqUrl("https://store.steampowered.com/specials?cc=us&l=english")

    def test_getDailyGamesUrls(self):
        """ Verifica se o método getDailyGamesUrls() em inglês está 
        funcionando corretamente.
        
        """

        urls = getDailyGamesUrls(self.soup)

        self.assertIsInstance(urls, list)
        self.assertGreaterEqual(len(urls), 0)
        
if __name__ == "__main__":
    unittest.main()