from bs4 import BeautifulSoup
from re import sub

def getRecommendationByPriceRangeOriginalPrices(soup: BeautifulSoup) -> list:
    """ Função responsável por retornar uma lista contendo os preços originais 
    dos jogos que estão na faixa de preço especificada.

    Parameters
    -----------
    soup: :class:`BeautifulSoup`

    Returns
    -----------
    originalPrices: :class:`list`
    """
    
    originalPrices = []

    for listDivGamesPrices in soup.find_all('div', class_='search_price'):
        if(listDivGamesPrices.contents[0] == '\n'):
            if(len(listDivGamesPrices.contents) == 4):
                
                for listSpanGamesPrices in listDivGamesPrices.find_all('span'):
                    originalPrices.append(listSpanGamesPrices.contents[0].contents[0])
            else:
                originalPrices.append("Não disponível!")
        else:
            temp = sub(r"\s+", "" , listDivGamesPrices.contents[0])

            if(temp == "Gratuitoparajogar" or temp == "Gratuitop/Jogar"):
                temp = "Gratuito para jogar"
                
            originalPrices.append(temp)

    return originalPrices