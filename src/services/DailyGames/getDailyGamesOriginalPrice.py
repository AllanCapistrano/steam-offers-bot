from bs4 import BeautifulSoup

def getDailyGamesOriginalPrice(soup: BeautifulSoup) -> list:
        """ Função responsável por retornar uma lista contendo os preços originais
        dos jogos que estão em promoção.

        Parameters
        -----------
        soup: :class:`BeautifulSoup`

        Returns
        -----------
        originalPrices: :class:`list`
        """
        
        originalPrices = []

        for dailyGames in soup.find_all('div', class_='dailydeal_ctn'):
            dailyGamesPrices = dailyGames.find_all('div', class_='discount_prices')
            temp = str(dailyGamesPrices).split('>')
            
            # Caso não tenha nenhum preço para o jogo.
            try:
                temp1 = temp[2].split('</div')
            except:
                temp1 = ["Não disponível!"]

            originalPrices.append(temp1[0])

        return originalPrices