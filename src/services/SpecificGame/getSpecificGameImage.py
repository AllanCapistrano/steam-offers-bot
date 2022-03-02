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

    try:
        temp = soup.find("img").attrs["srcset"].split(" ")[2]
    except:
        temp = None
    
    return temp