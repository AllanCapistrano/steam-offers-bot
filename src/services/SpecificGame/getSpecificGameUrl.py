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

    try:
        temp = soup.attrs["href"]
        temp = temp[:len(temp) - 20] # Removendo ?snr=1_7_7_151_150_1 da URL
    except:
        temp = None
    
    return temp