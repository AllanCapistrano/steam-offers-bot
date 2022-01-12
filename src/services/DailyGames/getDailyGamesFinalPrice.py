from bs4 import BeautifulSoup

def getDailyGamesFinalPrice(soup: BeautifulSoup) -> list:
    """ Função responsável por retornar uma lista contendo os preços com o 
    desconto aplicado dos jogos que estão em promoção.

    Parameters
    -----------
    soup: :class:`BeautifulSoup`

    Returns
    -----------
    finalPrices: :class:`list`
    """
    
    finalPrices = []

    for dailyGames in soup.find_all("div", class_="dailydeal_ctn"):
        try:
            for dailyGamesPrices in dailyGames.find_all("div", class_="discount_prices"):
                finalPrices.append(dailyGamesPrices.find_all("div", class_="discount_final_price")[0].contents[0])
        except:
            finalPrices("Não disponível")
        
    return finalPrices