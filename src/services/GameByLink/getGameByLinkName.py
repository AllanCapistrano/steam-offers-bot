from bs4 import BeautifulSoup

def getGameByLinkName(soup: BeautifulSoup) -> str:
    """ Função responsável por retornar o nome do jogo.

    Parameters
    -----------
    soup: :class:`BeautifulSoup`

    Returns
    -----------
    name: :class:`str`
    """

    try:
        temp = soup.find(class_="apphub_AppName").contents[0]
    except:
        temp = None

    return temp