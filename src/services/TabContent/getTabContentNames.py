from bs4 import BeautifulSoup

def getTabContentNames(soup: BeautifulSoup) -> list:
        """ Função responsável por retornar uma lista contendo os nomes dos jogos
        que estão em uma aba específica.

        Parameters
        -----------
        soup: :class:`BeautifulSoup`

        Returns
        -----------
        names: :class:`list`
        """
        
        names = []

        for tabContent in soup.find_all('div', class_='tab_item_name'):
            names.append(tabContent.contents[0])

        return names