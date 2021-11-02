from bs4 import BeautifulSoup
from re import sub

def getGameByLinkOriginalPrice(soup: BeautifulSoup) -> str:
    """ Função responsável por retornar o preço original do jogo.

    Parameters
    -----------
    soup: :class:`BeautifulSoup`,

    Returns
    -----------
    originalPrice: :class:`str`
    """
    
    try:
        return soup.find(class_="discount_prices").contents[0].contents[0]
    except:
        temp = sub(r"\s+", "" , soup.find(class_="game_purchase_action_bg").contents[1].contents[0])
        
        if(temp.find('Gratuito') != -1):
            return "Gratuito p/ Jogar"
        
        if(not temp.replace("R$", "").split(",")[0].isnumeric()):
            return "Não disponível!"

        return temp