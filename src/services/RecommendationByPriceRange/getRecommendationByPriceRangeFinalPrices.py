from bs4 import BeautifulSoup
from re import sub

def getRecommendationByPriceRangeFinalPrices(soup: BeautifulSoup, language: str) -> list:
    """ Função responsável por retornar uma lista contendo os preços com 
    desconto dos jogos que estão na faixa de preço especificada.

    Parameters
    -----------
    soup: :class:`BeautifulSoup`
    language: :class: `str`
         Idioma que se deseja visualizar a página do jogo. 

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
                if(language == "brazilian"):
                    finalPrices.append("Não disponível!")
                elif(language == "english"):
                    finalPrices.append("Not available!")
        else:
            temp = sub(r"\s+", "" , listDivGamesPrices.contents[0])

            if(temp.find("Gratuito") != -1):
                temp = "Gratuito p/ jogar"
            elif(temp.find("Free") != -1):
                temp = "Free To Play"
                
            finalPrices.append(temp)

    return finalPrices