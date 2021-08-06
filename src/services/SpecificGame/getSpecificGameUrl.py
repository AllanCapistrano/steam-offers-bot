from bs4 import BeautifulSoup

def getSpecificGameUrl(soup: BeautifulSoup) -> str:
    """ Função responsável a url do jogo.

    Parameters
    -----------
    soup: :class:`BeautifulSoup`

    Returns
    -----------
    url: :class:`str`
    """
    
    return soup.attrs['href']