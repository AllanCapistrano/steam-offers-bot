from bs4 import BeautifulSoup

def getDailyGamesFinalPrice(soup: BeautifulSoup) -> list:
        """ Função responsável por retornar uma lista contendo os preços com o 
        desconto aplicado dos jogos que estão em promoção.

        Parameters
        -----------
        soup: :class:`BeautifulSoup`

        Returns
        -----------
        finalPrices: :class:`list`
        """
        
        finalPrices = []

        for dailyGames in soup.find_all('div', class_='dailydeal_ctn'):
            dailyGamesPrices = dailyGames.find_all('div', class_='discount_prices')
            temp = str(dailyGamesPrices).split('>')
            
            # Caso não tenha nenhum preço para o jogo.
            try:
                temp1 = temp[4].split('</div')
            except:
                temp1 = ["Não disponível!"]

            finalPrices.append(temp1[0])

        return finalPrices