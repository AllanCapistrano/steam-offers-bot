from bs4 import BeautifulSoup

def getSpotlightImages(soup: BeautifulSoup) -> list:
    """ Função responsável por retornar uma lista contendo as imagens dos 
    jogos que estão em destaque.

    Parameters
    -----------
    soup: :class:`BeautifulSoup`

    Returns
    -----------
    images: :class:`list`
    """
    
    images = []

    for spotlightGames in soup.find_all("div", class_="spotlight_img"):
        images.append(spotlightGames.contents[1].contents[1].attrs["src"])

    return images