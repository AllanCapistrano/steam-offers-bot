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
        dailyGamesPricesBlock = dailyGames.find_all("div", class_="discount_prices")
        
        if(len(dailyGamesPricesBlock) == 0):
            finalPrices.append("Não disponível!")
        else:
            for dailyGamesPrices in dailyGamesPricesBlock:
                finalPriceDiv = dailyGamesPrices.find_all("div", class_="discount_final_price")

                if(len(finalPriceDiv) > 0):
                    finalPrices.append(finalPriceDiv[0].contents[0])
                else:
                    finalPrices.append("Não disponível!")
        
    return finalPrices