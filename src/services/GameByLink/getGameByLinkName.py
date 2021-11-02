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

    return soup.find(class_="apphub_AppName").contents[0]