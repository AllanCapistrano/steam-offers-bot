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
        dailyGamesPricesBlock = dailyGames.find_all('div', class_='discount_prices')
        
        if(len(dailyGamesPricesBlock) == 0):
            originalPrices.append("Não disponível!")
        else:
            for dailyGamesPrices in dailyGamesPricesBlock:
                originalPrices.append(dailyGamesPrices.find_all("div", class_="discount_original_price")[0].contents[0])

    return originalPrices