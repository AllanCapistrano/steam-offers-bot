from bs4 import BeautifulSoup

def getRecommendationByPriceRangeNames(soup: BeautifulSoup) -> list:
        """ Função responsável por retornar uma lista contendo os nomes dos jogos
        que estão na faixa de preço especificada.

        Parameters
        -----------
        soup: :class:`BeautifulSoup`

        Returns
        -----------
        names: :class:`list`
        """
        
        names = []

        for listDivGamesNames in soup.find_all('div', class_="search_name"):
            for listSpanGamesNames in listDivGamesNames.find_all('span', class_="title"):
                names.append(listSpanGamesNames.contents[0])

        return names