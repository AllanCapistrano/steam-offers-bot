from bs4 import BeautifulSoup
from re import sub

def getSpecificGameOriginalPrice(soup: BeautifulSoup, haveDiscount: bool, language: str) -> str:
    """ Função responsável por retornar o preço original do jogo.

    Parameters
    -----------
    soup: :class:`BeautifulSoup`,
    haveDiscount :class:`bool`
    language: :class: `str`
         Idioma que se deseja visualizar a página do jogo. 

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
                if(language == "brazilian"):
                    return "Não disponível!"
                elif(language == "english"):
                    return "Not available!"

            temp = sub(r"\s+", "" , searchPrice)

            if(temp.find("Gratuito") != -1):
                return "Gratuito p/ Jogar"
            elif(temp.find("Free") != -1):
                return "Free To Play"
            
            return temp
        except:
            if(language == "brazilian"):
                return "Não disponível!"
            elif(language == "english"):
                return "Not available!"