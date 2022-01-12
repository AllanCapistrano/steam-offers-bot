from bs4 import BeautifulSoup

def getDailyGamesUrls(soup: BeautifulSoup) -> list:
    """ Função responsável por retornar uma lista contendo as urls dos jogos
    que estão em promoção.

    Parameters
    -----------
    soup: :class:`BeautifulSoup`

    Returns
    -----------
    urls: :class:`list`
    """

    urls = []

    for dailyGames in soup.find_all("div", class_="dailydeal_cap"):
        urls.append(dailyGames.contents[1].attrs["href"])

    return urls