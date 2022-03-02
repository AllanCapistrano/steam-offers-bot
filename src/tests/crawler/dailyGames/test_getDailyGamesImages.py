from sys import path
path.append("../../../") # Habilita a importação dos arquivo que etão em src/*

import unittest
from services.crawler import Crawler
from services.DailyGames.getDailyGamesImages import getDailyGamesImages

class TestGetDailyGamesImages(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.crawler = Crawler()
        self.soup    = self.crawler.reqUrl("https://store.steampowered.com/specials?cc=us&l=english")

    def test_getDailyGamesImages(self):
        """ Verifica se o método getDailyGamesImages() em inglês está 
        funcionando corretamente.
        
        """

        images = getDailyGamesImages(self.soup)

        self.assertIsInstance(images, list)
        self.assertGreaterEqual(len(images), 0)
        
if __name__ == "__main__":
    unittest.main()