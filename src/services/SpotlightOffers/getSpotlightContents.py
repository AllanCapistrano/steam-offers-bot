from bs4 import BeautifulSoup

def getSpotlightContents(soup: BeautifulSoup) -> list:
        """ Função responsável por retornar uma lista contendo as informações dos 
        jogos que estão em destaque.

        Parameters
        -----------
        soup: :class:`BeautifulSoup`

        Returns
        -----------
        contents: :class:`list`
        """
        
        contents = []

        for spotlightGames in soup.find_all('div', class_='spotlight_content'):
            contentDict = {
                "id": spotlightGames.parent.attrs["id"], 
                "value": spotlightGames.contents[1].contents[0]
            }

            contents.append(contentDict)

        return contents