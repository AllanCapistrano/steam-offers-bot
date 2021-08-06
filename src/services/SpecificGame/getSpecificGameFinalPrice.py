from bs4 import BeautifulSoup
from re import sub

def getSpecificGameFinalPrice(soup: BeautifulSoup, haveDiscount: bool) -> str:
        """ Função responsável o preço com desconto do jogo.

        Parameters
        -----------
        soup: :class:`BeautifulSoup`,
        haveDiscount :class:`bool`

        Returns
        -----------
        url: :class:`str`
        """
        
        if(haveDiscount):
            return  sub(r"\s+", "" , soup.find(class_='search_price').contents[3])
        else:
            temp = sub(r"\s+", "" , soup.find(class_='search_price').contents[0])

            if(temp.find('Gratuito') != -1):
                return "Gratuiro p/ Jogar"

            if(not temp.replace("R$", "").split(",")[0].isnumeric()):
                return "Não disponível!"

            return temp