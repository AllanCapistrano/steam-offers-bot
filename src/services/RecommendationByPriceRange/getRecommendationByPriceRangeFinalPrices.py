from bs4 import BeautifulSoup
from re import sub

def getRecommendationByPriceRangeFinalPrices(soup: BeautifulSoup) -> list:
    """ Função responsável por retornar uma lista contendo os preços com 
    desconto dos jogos que estão na faixa de preço especificada.

    Parameters
    -----------
    soup: :class:`BeautifulSoup`

    Returns
    -----------
    finalPrices: :class:`list`
    """
    
    finalPrices = []

    for listDivGamesPrices in soup.find_all("div", class_="search_price"):
        if(listDivGamesPrices.contents[0] == "\n"):
            if(len(listDivGamesPrices.contents) == 4):
                temp = sub(r"\s+", "" , listDivGamesPrices.contents[3])
                finalPrices.append(temp)
            else:
                finalPrices.append("Não disponível!")
        else:
            temp = sub(r"\s+", "" , listDivGamesPrices.contents[0])

            if(temp.find("Gratuito") != -1):
                temp = "Gratuito p/ jogar"
                
            finalPrices.append(temp)

    return finalPrices