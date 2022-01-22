from bs4 import BeautifulSoup
from re import sub

def getSpecificGameOriginalPrice(soup: BeautifulSoup, haveDiscount: bool) -> str:
    """ Função responsável por retornar o preço original do jogo.

    Parameters
    -----------
    soup: :class:`BeautifulSoup`,
    haveDiscount :class:`bool`

    Returns
    -----------
    url: :class:`str`
    """
    
    if(haveDiscount):
        return soup.find(class_="search_price").contents[1].contents[0].contents[0]
    else:
        try:
            searchPrice = soup.find(class_="search_price").contents[0]

            if(searchPrice == "\n"):
                return "Não disponível!"

            temp = sub(r"\s+", "" , searchPrice)

            if(temp.find("Gratuito") != -1):
                return "Gratuito p/ Jogar"
            
            return temp
        except:
            return "Não disponível!"