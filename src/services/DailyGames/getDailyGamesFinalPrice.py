from bs4 import BeautifulSoup

def getDailyGamesFinalPrice(soup: BeautifulSoup, language: str) -> list:
    """ Função responsável por retornar uma lista contendo os preços com o 
    desconto aplicado dos jogos que estão em promoção.

    Parameters
    -----------
    soup: :class:`BeautifulSoup`
    language: :class:`str`
        Idioma que se deseja visualizar a página do jogo.

    Returns
    -----------
    finalPrices: :class:`list`
    """
    
    finalPrices = []

    for dailyGames in soup.find_all("div", class_="dailydeal_ctn"):
        dailyGamesPricesBlock = dailyGames.find_all("div", class_="discount_prices")

        if(len(dailyGamesPricesBlock) == 0):
            if(language == "brazilian"):
                finalPrices.append("Não disponível!")
            elif(language == "english"):
                finalPrices.append("Not available!")
        else:
            for dailyGamesPrices in dailyGamesPricesBlock:
                finalPriceDiv = dailyGamesPrices.find_all("div", class_="discount_final_price")

                if(len(finalPriceDiv) > 0):
                    finalPrices.append(finalPriceDiv[0].contents[0])
                else:
                    if(language == "brazilian"):
                        finalPrices.append("Não disponível!")
                    elif(language == "english"):
                        finalPrices.append("Not available!")
        
    return finalPrices