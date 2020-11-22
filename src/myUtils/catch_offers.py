import requests
from bs4 import BeautifulSoup

URL_MAIN = 'https://store.steampowered.com/?l=brazilian'
URL_SPECIALS = 'https://store.steampowered.com/specials?l=brazilian'


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
        soup = self.reqUrl(URL_SPECIALS)

        for list_games in soup.find_all('div', class_='dailydeal_cap'):
            gamesURL.append(list_games.contents[1].attrs['href'])
            gamesIMG.append(list_games.contents[1].contents[1].attrs['src'])

        return gamesURL, gamesIMG

    # Função que retorna duas listas, uma contendo o preço original dos jogos, e
    # a outra contendo o preço com o desconto aplicado.
    def getDailyGamesOffersPrices(self):
        gameOriginalPrice = []
        gameFinalPrice = []
        soup = self.reqUrl(URL_SPECIALS)

        for list_prices in soup.find_all('div', class_='dailydeal_ctn'):
            list_p = list_prices.find_all('div', class_='discount_prices')
            x = str(list_p).split('>')
            # Caso não tenha nenhum preço para o jogo.
            try:
                y = x[2].split('</div')
                z = x[4].split('</div')
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
        soup = self.reqUrl(URL_SPECIALS)

        for list_games in soup.find_all('div', class_='spotlight_img'):
            gamesURL.append(list_games.contents[1].attrs['href'])
            gamesIMG.append(list_games.contents[1].contents[1].attrs['src'])

        for list_content in soup.find_all('div', class_='spotlight_content'):
            gamesH2.append(list_content.contents[1].contents[0])

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
                gamesNames.append(list_g.contents[0])
            # Responsável por pegar as URLs do jogos/DLCs que estão em promoção.
            for list_g in list_games.find_all('a', class_='tab_item'):
                gamesURL.append(list_g.attrs['href'])
            # Responsável por pegar os preços originais e com desconto dos jogos/DLCs que estão em promoção.
            for list_prices in list_games.find_all('div', class_='discount_prices'):
                gameOriginalPrice.append(list_prices.contents[0].contents[0])
                gameFinalPrice.append(list_prices.contents[1].contents[0])

        return gamesNames, gamesURL, gameOriginalPrice, gameFinalPrice