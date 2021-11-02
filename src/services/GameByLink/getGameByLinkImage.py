from bs4 import BeautifulSoup

def getGameByLinkImage(soup: BeautifulSoup) -> str:
    """ Função responsável a imagem do jogo.

    Parameters
    -----------
    soup: :class:`BeautifulSoup`

    Returns
    -----------
    image: :class:`str`
    """
    
    return soup.find(class_="game_header_image_ctn").contents[1].attrs["src"].replace("header", "capsule_231x87")