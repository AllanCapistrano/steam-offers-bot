from bs4 import BeautifulSoup
from re import sub

def getRecommendationByPriceRangeOriginalPrices(soup: BeautifulSoup, language: str) -> list:
    """ Função responsável por retornar uma lista contendo os preços originais 
    dos jogos que estão na faixa de preço especificada.

    Parameters
    -----------
    soup: :class:`BeautifulSoup`
    language: :class: `str`
         Idioma que se deseja visualizar a página do jogo. 


    Returns
    -----------
    originalPrices: :class:`list`
    """
    
    originalPrices = []

    for listDivGamesPrices in soup.find_all("div", class_="search_price"):
        if(listDivGamesPrices.contents[0] == "\n"):
            if(len(listDivGamesPrices.contents) == 4):
                for listSpanGamesPrices in listDivGamesPrices.find_all("span"):
                    originalPrices.append(listSpanGamesPrices.contents[0].contents[0])
            else:
                if(language == "brazilian"):
                    originalPrices.append("Não disponível!")
                elif(language == "english"):
                    originalPrices.append("Not available!")
        else:
            temp = sub(r"\s+", "" , listDivGamesPrices.contents[0])

            if(temp.find("Gratuito") != -1):
                temp = "Gratuito p/ jogar"
            elif(temp.find("Free") != -1):
                temp = "Free To Play"
                
            originalPrices.append(temp)

    return originalPrices