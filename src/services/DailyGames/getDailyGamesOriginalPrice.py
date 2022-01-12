from bs4 import BeautifulSoup

def getDailyGamesOriginalPrice(soup: BeautifulSoup) -> list:
    """ Função responsável por retornar uma lista contendo os preços originais
    dos jogos que estão em promoção.

    Parameters
    -----------
    soup: :class:`BeautifulSoup`

    Returns
    -----------
    originalPrices: :class:`list`
    """
    
    originalPrices = []

    for dailyGames in soup.find_all('div', class_='dailydeal_ctn'):
        for dailyGamesPrices in dailyGames.find_all('div', class_='discount_prices'):
            try:
                originalPrices.append(dailyGamesPrices.find_all("div", class_="discount_original_price")[0].contents[0])
            except:
                originalPrices("Não disponível")

    return originalPrices