import requests
from bs4 import BeautifulSoup

URL = 'https://store.steampowered.com/specials?l=brazilian'
CURRENCY = 'US'


class CatchOffers:
    # Função para buscar o site pela URL
    def reqUrl(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        return soup

    # Função que retorna duas listas, uma contendo a URL dos jogos que estão na
    # promoção diária, e a outra contendo a imagem do banner dos jogos que estão na promoção diária.
    def getDailyGamesOffers(self):
        gamesURL = []
        gamesIMG = []
        soup = self.reqUrl(URL)

        for list_games in soup.find_all('div', class_='dailydeal_cap'):
            list_g = list_games.find_all('a')
            x = str(list_g).split('"')
            gamesURL.append(x[1])
            gamesIMG.append(x[3])

        return gamesURL, gamesIMG

    # Função que retorna duas listas, uma contendo o preço original dos jogos, e
    # a outra contendo o preço com o desconto aplicado.
    def getDailyGamesOffersPrices(self):
        gameOriginalPrice = []
        gameFinalPrice = []
        soup = self.reqUrl(URL)

        for list_prices in soup.find_all('div', class_='dailydeal_ctn'):
            list_p = list_prices.find_all('div', class_='discount_prices')
            x = str(list_p).split('>')
            # Caso não tenha nenhum preço para o jogo.
            try:
                y = x[2].split('</div')
                z = x[4].split('</div')
                y[0] = CURRENCY + y[0]
                z[0] = CURRENCY + z[0]
            except:
                y = ["Não disponível!"]
                z = ["Não disponível!"]

            gameOriginalPrice.append(y[0])
            gameFinalPrice.append(z[0])

        return gameOriginalPrice, gameFinalPrice

    # Função que retorna três listas, uma contendo a URL, outra contendo as imagens,
    # e por fim, outra contendo a descrição do evento/jogo em destaque.
    def getSpotlightOffers(self):
        gamesURL = []
        gamesIMG = []
        gamesH2 = []
        soup = self.reqUrl(URL)

        for list_games in soup.find_all('div', class_='spotlight_img'):
            list_g = list_games.find_all('a')
            x = str(list_g).split('"')
            gamesURL.append(x[1])
            gamesIMG.append(x[7])

        for list_content in soup.find_all('div', class_='spotlight_content'):
            list_c = list_content.find_all('h2')
            x = str(list_c).split('>')
            # Caso não tenha uma descrição para o evento/jogo dentro de uma tag h2.
            try:
                y = x[1].split('</h2')
            except:
                y = ["Não há descrição"]

            gamesH2.append(y[0])

        return gamesURL, gamesIMG, gamesH2

    # Função que retorna quatro listas que possuem respectivamente as seguintes
    # informações: nome, URL, preço original, e preço com desconto; dos jogos/DLCs que estão em promoção.
    def getTabContent(self, url, divId):
        gamesNames = []
        gamesURL = []
        gameOriginalPrice = []
        gameFinalPrice = []
        soup = self.reqUrl(url)

        for list_games in soup.find_all('div', id=divId):
            # Responsável por pegar os nomes dos jogos/DLCs que estão promoção.
            for list_g in list_games.find_all('div', class_='tab_item_name'):
                x = str(list_g).split('>')
                y = x[1].split('</div')
                gamesNames.append(y[0])
            # Responsável por pegar as URLs do jogos/DLsC que estão em promoção.
            for list_g in list_games.find_all('a', class_='tab_item'):
                x = str(list_g).split('href="')
                y = x[1].split('"')
                gamesURL.append(y[0])
            # Responsável por pegar os preços originais e com desconto dos jogos/DLCs que estão em promoção.
            for list_prices in list_games.find_all('div', class_='discount_prices'):
                x = str(list_prices).split('>')
                y = x[2].split('</div')
                z = x[4].split('</div')
                y[0] = CURRENCY + y[0]
                z[0] = CURRENCY + z[0]
                gameOriginalPrice.append(y[0])
                gameFinalPrice.append(z[0])

        return gamesNames, gamesURL, gameOriginalPrice, gameFinalPrice
