from bs4 import BeautifulSoup

def getTabContentOriginalPrices(soup: BeautifulSoup) -> list:
    """ Função responsável por retornar uma lista contendo os preços 
    originais dos jogos que estão em uma aba específica.

    Parameters
    -----------
    soup: :class:`BeautifulSoup`

    Returns
    -----------
    orginalPrices: :class:`list`
    """
    
    orginalPrices = []

    for tabContent in soup.find_all('div', class_='discount_prices'):                
        if(len(tabContent) == 2):
            orginalPrices.append(tabContent.contents[0].contents[0])
        elif(len(tabContent) == 1):
            temp = tabContent.contents[0].contents[0]

            if(temp.find('Free to Play') != -1 or temp.find('Free') != -1):
                temp = "Gratuiro p/ Jogar"

            orginalPrices.append(temp)

    return orginalPrices