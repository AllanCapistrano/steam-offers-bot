from bs4 import BeautifulSoup

def getSpecificGameName(soup: BeautifulSoup) -> str:
    """ Função responsável por retornar o nome do jogo como está na Steam.

    Parameters
    -----------
    soup: :class:`BeautifulSoup`

    Returns
    -----------
    name: :class:`str`
    """

    try:
        temp = soup.find(class_="search_name").contents[1].contents[0]
    except:
        temp = None
    
    return temp