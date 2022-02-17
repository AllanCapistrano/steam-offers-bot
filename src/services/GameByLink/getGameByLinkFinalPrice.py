from bs4 import BeautifulSoup
from re import sub

def getGameByLinkFinalPrice(soup: BeautifulSoup, language: str) -> str:
    """ Função responsável por retornar o preço com desconto, caos tenha, do 
    jogo.

    Parameters
    -----------
    soup: :class:`BeautifulSoup`
    language: :class: `str`
         Idioma que se deseja visualizar a página do jogo. 

    Returns
    -----------
    originalPrice: :class:`str`
    """
    
    try:
        return soup.find(class_="discount_prices").contents[1].contents[0]
    except:
        try:
            searchPrice = soup.find(class_="game_purchase_action_bg").contents[1].contents[0]

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