from bs4 import BeautifulSoup

def getRecommendationByPriceRangeUrls(soup: BeautifulSoup) -> list:
    """ Função responsável por retornar uma lista contendo as urls dos jogos 
    que estão na faixa de preço especificada.

    Parameters
    -----------
    soup: :class:`BeautifulSoup`

    Returns
    -----------
    urls: :class:`list`
    """
    
    urls = []

    for listAGamesUrls in soup.find_all("a", class_="search_result_row"):
        urls.append(listAGamesUrls.attrs["href"])

    return urls