from bs4 import BeautifulSoup

def getTabContentHasPrice(soup: BeautifulSoup) -> tuple[list, bool]:
        """ Função responsável por retornar uma lista que indica a posição dos
        jogos que não possuem nenhuma precificação (caso exista).

        Parameters
        -----------
        soup: :class:`BeautifulSoup`

        Returns
        -----------
        hasPrice: :class:`list`
        gameWithoutPricing: :class:`bool`
        """
        
        hasPrice           = []
        gameWithoutPricing = False

        for tabContent in soup.find_all('div', class_='discount_block'):
            try:
                tabContent['class'].index("empty")
                hasPrice.append(False)
                
                gameWithoutPricing = True
            except:
                hasPrice.append(True)

        return hasPrice, gameWithoutPricing