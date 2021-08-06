from bs4 import BeautifulSoup

def getTabContentUrls(soup: BeautifulSoup) -> list:
        """ Função responsável por retornar uma lista contendo as urls dos jogos
        que estão em uma aba específica.

        Parameters
        -----------
        soup: :class:`BeautifulSoup`

        Returns
        -----------
        urls: :class:`list`
        """
        
        urls = []

        for tabContent in soup.find_all('a', class_='tab_item'):
            urls.append(tabContent.attrs['href'])

        return urls