from bs4 import BeautifulSoup

def getSpotlightUrls(soup: BeautifulSoup) -> list:
    """ Função responsável por retornar uma lista contendo as URLs dos jogos
    que estão em destaque.

    Parameters
    -----------
    soup: :class:`BeautifulSoup`

    Returns
    -----------
    urls: :class:`list`
    """

    urls = []

    for spotlightGames in soup.find_all("div", class_="spotlight_img"):
        urlDict = {
            "id": spotlightGames.parent.attrs["id"], 
            "value": spotlightGames.contents[1].attrs["href"]
        }

        urls.append(urlDict)

    return urls