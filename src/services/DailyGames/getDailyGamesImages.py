from bs4 import BeautifulSoup

def getDailyGamesImages(soup: BeautifulSoup) -> list:
        """ Função responsável por retornar uma lista contendo as imagens dos 
        jogos que estão em promoção.

        Parameters
        -----------
        soup: :class:`BeautifulSoup`

        Returns
        -----------
        images: :class:`list`
        """
        
        images = []

        for dailyGames in soup.find_all('div', class_='dailydeal_cap'):
            images.append(dailyGames.contents[1].contents[1].attrs['src'])

        return images