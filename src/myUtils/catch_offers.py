from re import sub
from random import randint

import requests
from bs4 import BeautifulSoup

from myUtils.tabContent import TabContent
from myUtils.tabContentRow import TabContentRow

URL_MAIN = 'https://store.steampowered.com/?cc=br&l=brazilian'
URL_SPECIALS = 'https://store.steampowered.com/specials?cc=br&l=brazilian'
URL_GAME = 'https://store.steampowered.com/search/?cc=br&l=brazilian&term='
URL_GENRE = 'https://store.steampowered.com/tags/pt-br/'
# URL_PRICE_RANGE = 'https://store.steampowered.com/search/?maxprice='
URL_PRICE_RANGE = 'https://store.steampowered.com/search/?l=brazilian'
class CatchOffers:
    # Função para buscar o site pela URL
    def reqUrl(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        return soup

    # Função que retorna duas listas, uma contendo a URL dos jogos que estão na
    # promoção diária, e a outra contendo a imagem do banner dos jogos que estão 
    # na promoção diária.
    async def getDailyGamesOffers(self):
        gamesURL = []
        gamesIMG = []
        soup = self.reqUrl(URL_SPECIALS)

        for list_games in soup.find_all('div', class_='dailydeal_cap'):
            gamesURL.append(list_games.contents[1].attrs['href'])
            gamesIMG.append(list_games.contents[1].contents[1].attrs['src'])

        return gamesURL, gamesIMG

    # Função que retorna duas listas, uma contendo o preço original dos jogos, e
    # a outra contendo o preço com o desconto aplicado.
    async def getDailyGamesOffersPrices(self):
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
    async def getSpotlightOffers(self):
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

    # Função que retorna cinco listas que possuem respectivamente as seguintes
    # informações: nome, URL, preço original, preço com desconto e imagens; 
    # dos jogos/DLCs de uma categoria.
    async def getTabContent(self, url, divId):
        hasPrice = []
        gameWithoutPricing = False
        gamesNames = []
        gamesURL = []
        gameOriginalPrice = []
        gameFinalPrice = []
        gameIMG = []
        soup = self.reqUrl(url)

        for list_games in soup.find_all('div', id=divId):
            # Responsável por pegar os nomes dos jogos/DLCs de uma categoria.
            for list_g in list_games.find_all('div', class_='tab_item_name'):
                gamesNames.append(list_g.contents[0])
            # Responsável por pegar as URLs do jogos/DLCs de uma categoria.
            for list_g in list_games.find_all('a', class_='tab_item'):
                gamesURL.append(list_g.attrs['href'])

            # Responsável por verificar se existe a classe empty em algum jogo. 
            # Se existir, o jogo não possui precificação, e o mesmo é marcado.
            for listHasPrice in list_games.find_all('div', class_='discount_block'):
                try:
                    listHasPrice['class'].index("empty")
                    hasPrice.append(False)
                    gameWithoutPricing = True
                except:
                    hasPrice.append(True)

            # Responsável por pegar os preços originais e com desconto 
            # (caso exista) dos jogos/DLCs de uma categoria.
            for list_prices in list_games.find_all('div', class_='discount_prices'):                
                if(len(list_prices) == 2):
                    gameOriginalPrice.append(list_prices.contents[0].contents[0])
                    gameFinalPrice.append(list_prices.contents[1].contents[0])
                elif(len(list_prices) == 1):
                    temp = list_prices.contents[0].contents[0]

                    if(temp.find('Free to Play') != -1 or temp.find('Free') != -1):
                        temp = "Gratuiro p/ Jogar"

                    gameOriginalPrice.append(temp)
                    gameFinalPrice.append(temp)

            # Responsável por pegar as imagens dos jogos/DLCs de uma categoria.
            for list_gamesIMG in list_games.find_all('img', class_='tab_item_cap_img'):
                # Mudando o tamanho da imagem.
                img = list_gamesIMG.attrs['src'].replace("184x69", "231x87")

                gameIMG.append(img)

        # Verifica se há pelo menos um jogo sem preço. Em caso positivo, adiciona
        # essa infomaçã na posição correta da lista.
        if(gameWithoutPricing):
            for x in range(len(hasPrice) - 1):
                if(not hasPrice[x]):
                    gameOriginalPrice.insert(x, 'Preço indisponível!')
                    gameFinalPrice.insert(x, 'Preço indisponível!')

        return gamesNames, gamesURL, gameOriginalPrice, gameFinalPrice, gameIMG

    #Função que retorna o nome, o preço, o link e a imagem de um jogo específico.
    async def getSpecificGame(self, gameName):
        gamePrice = []
        searchUrl = URL_GAME + gameName
        soup = self.reqUrl(searchUrl)

        try:
            game = soup.find(id='search_resultsRows').find(class_='search_result_row ds_collapse_flag')

            gameURL = game.attrs['href']
            gameIMG = game.find('img').attrs['srcset'].split(" ")[2]
            gameName = game.find(class_='search_name').contents[1].contents[0]

            haveDiscount = True if len(game.find(class_='search_price').contents) > 1 else False

            if(haveDiscount):
                gamePrice.append(game.find(class_='search_price').contents[1].contents[0].contents[0])
                temp = sub(r"\s+", "" , game.find(class_='search_price').contents[3])
                gamePrice.append(temp)
            else:
                temp = sub(r"\s+", "" , game.find(class_='search_price').contents[0])
                
                if(temp.find('Gratuito') != -1):
                    temp = "Gratuiro p/ Jogar"

                gamePrice.append(temp)
        except:
            gameName = gameURL = gameIMG = gamePrice = None

        return gameName, gameURL, gameIMG, gamePrice, searchUrl.replace(" ", "%20")

    # Função que retorna um jogo recomendado de um gênero específico.
    async def getGameRecommendationByGenre(self, genre):
        if(genre == 'acao'):
            genre = 'ação'
        elif(genre == 'estrategia'):
            genre = 'estratégia'
        elif(
            genre == 'multijogador massivo' or 
            genre == 'Multijogador massivo' or 
            genre == 'multijogador Massivo' or 
            genre == 'Multijogador Massivo'
        ):
            genre = 'multijogador%20massivo'
        elif(genre == 'simulacao'):
            genre = 'simulação'

        pos = randint(0, len(TabContent) - 1)
        tabContent = TabContent(pos).name
        tabContentRow = TabContentRow(pos).name

        url = URL_GENRE + '{}/?cc=br#p=0&tab={}'.format(genre, tabContent)

        try:
            (
                list_gameNames, 
                list_gameURLs, 
                list_gameOriginalPrices, 
                list_gameFinalPrices, list_gameIMGs
            ) = await self.getTabContent(url, tabContentRow)
            
            number = randint(0, len(list_gameNames) - 1)

            gameName = list_gameNames[number]
            gameURL = list_gameURLs[number]
            gameOriginalPrice = list_gameOriginalPrices[number]
            gameFinalPrice = list_gameFinalPrices[number]
            gameIMG = list_gameIMGs[number]
        except:
            gameName = gameURL = gameOriginalPrice = gameFinalPrice = gameIMG = None

        return gameName, gameURL, gameOriginalPrice, gameFinalPrice, gameIMG

    # Função que retorna um jogo recomendado a partir de uma faixa de preço.
    async def getGameRecommendationByPriceRange(self, maxPrice):
        if(maxPrice == "rZ04j"):
            url = URL_PRICE_RANGE
        else:
            url = URL_PRICE_RANGE + '&maxprice={}&cc=br'.format(maxPrice)
        
        soup = self.reqUrl(url)

        list_gamesNames = []
        list_gamesImgs = []
        list_gameOriginalPrice = []
        list_gameFinalPrice = []
        list_gamesUrls = []

        gamePrice = []

        for listDivGamesNames in soup.find_all('div', class_="search_name"):
            for listSpanGamesNames in listDivGamesNames.find_all('span', class_="title"):
                list_gamesNames.append(listSpanGamesNames.contents[0])

        for listDivGamesImages in soup.find_all('div', class_="search_capsule"):
            for listImgGamesImages in listDivGamesImages.find_all('img'):
                img = listImgGamesImages.attrs['srcset'].split(" ")[2]
                list_gamesImgs.append(img)
        
        for listDivGamesPrices in soup.find_all('div', class_='search_price'):
            if(listDivGamesPrices.contents[0] == '\n'):
                if(len(listDivGamesPrices.contents) == 4):
                    temp = sub(r"\s+", "" , listDivGamesPrices.contents[3])
                    list_gameFinalPrice.append(temp)
                    
                    for listSpanGamesPrices in listDivGamesPrices.find_all('span'):
                        list_gameOriginalPrice.append(listSpanGamesPrices.contents[0].contents[0])
                else:
                    list_gameFinalPrice.append("Não disponível!")
                    list_gameOriginalPrice.append("Não disponível!")
            else:
                temp = sub(r"\s+", "" , listDivGamesPrices.contents[0])

                if(temp == "Gratuitoparajogar" or temp == "Gratuitop/Jogar"):
                    temp = "Gratuito para jogar"
                    
                list_gameOriginalPrice.append(temp)
                list_gameFinalPrice.append(temp)

        for listAGamesUrls in soup.find_all('a', class_="search_result_row"):
            list_gamesUrls.append(listAGamesUrls.attrs['href'])

        number = randint(0, len(list_gamesNames) - 1)

        gameName = list_gamesNames[number]
        gameImg = list_gamesImgs[number]
        gameUrl = list_gamesUrls[number]
        gamePrice.append(list_gameOriginalPrice[number])
        gamePrice.append(list_gameFinalPrice[number])

        return gameName, gameImg, gameUrl, gamePrice