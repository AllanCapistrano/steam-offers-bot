from bs4 import BeautifulSoup

def getSpecificGameImage(soup: BeautifulSoup) -> str:
        """ Função responsável a imagem do jogo.

        Parameters
        -----------
        soup: :class:`BeautifulSoup`

        Returns
        -----------
        image: :class:`str`
        """
        
        return soup.find('img').attrs['srcset'].split(" ")[2]