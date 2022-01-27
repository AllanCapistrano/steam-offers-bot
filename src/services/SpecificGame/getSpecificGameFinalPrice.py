from bs4 import BeautifulSoup
from re import sub

def getSpecificGameFinalPrice(soup: BeautifulSoup, haveDiscount: bool) -> str:
    """ Função responsável por retornar o preço com desconto do jogo.

    Parameters
    -----------
    soup: :class:`BeautifulSoup`,
    haveDiscount :class:`bool`

    Returns
    -----------
    url: :class:`str`
    """
    
    if(haveDiscount):
        return soup.find(class_="search_price").contents[3]
    else:
        try:
            searchPrice = soup.find(class_="search_price").contents[0]

            if(searchPrice == "\n"):
                return "Não disponível!"

            temp = sub(r"\s+", "" , searchPrice)

            if(temp.find("Gratuito") != -1):
                return "Gratuito p/ Jogar"
            elif(temp.find("Free") != -1):
                return "Free To Play"
            
            return temp
        except:
            return "Não disponível!"