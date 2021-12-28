from bs4 import BeautifulSoup
from re import sub

def getGameByLinkFinalPrice(soup: BeautifulSoup) -> str:
    """ Função responsável por retornar o preço com desconto, caos tenha, do 
    jogo.

    Parameters
    -----------
    soup: :class:`BeautifulSoup`,

    Returns
    -----------
    originalPrice: :class:`str`
    """
    
    try:
        return soup.find(class_="discount_prices").contents[1].contents[0]
    except:
        try:
            temp = sub(r"\s+", "" , soup.find(class_="game_purchase_action_bg").contents[1].contents[0])

            if(temp.find('Gratuito') != -1):
                return "Gratuito p/ Jogar"
            
            if(not temp.replace("R$", "").split(",")[0].isnumeric()):
                return "Não disponível!"

            return temp
        except:
            return "Não disponível!"