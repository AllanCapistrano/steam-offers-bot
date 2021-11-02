from bs4 import BeautifulSoup
from re import sub

def getSpecificGameOriginalPrice(soup: BeautifulSoup, haveDiscount: bool) -> str:
    """ Função responsável o preço original do jogo.

    Parameters
    -----------
    soup: :class:`BeautifulSoup`,
    haveDiscount :class:`bool`

    Returns
    -----------
    url: :class:`str`
    """
    
    if(haveDiscount):
        return soup.find(class_='search_price').contents[1].contents[0].contents[0]
    else:
        temp = sub(r"\s+", "" , soup.find(class_='search_price').contents[0])

        if(temp.find('Gratuito') != -1):
            return "Gratuito p/ Jogar"
        
        if(not temp.replace("R$", "").split(",")[0].isnumeric()):
            return "Não disponível!"

        return temp