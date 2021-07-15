from re import sub
from random import randint
import concurrent.futures
import requests
from bs4 import BeautifulSoup

from myUtils.tabContent import TabContent
from myUtils.tabContentRow import TabContentRow

URL_MAIN = 'https://store.steampowered.com/?cc=br&l=brazilian'
URL_SPECIALS = 'https://store.steampowered.com/specials?cc=br&l=brazilian'
URL_GAME = 'https://store.steampowered.com/search/?cc=br&l=brazilian&term='
URL_GENRE = 'https://store.steampowered.com/tags/pt-br/'
URL_PRICE_RANGE = 'https://store.steampowered.com/search/?l=brazilian'
class CatchOffers:
    # Função para buscar o site pela URL
    def reqUrl(self, url: str):
        r    = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        
        return soup

    # Função que retorna quatro listas, uma contendo a URL dos jogos que estão na
    # promoção diária, outra contendo a imagem do banner dos jogos que estão 
    # na promoção diária, outra contendo o preço original dos jogos, e por fim 
    # uma contendo preço com o desconto aplicado.
    async def getDailyGamesOffers(self):
        soup = self.reqUrl(URL_SPECIALS)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            thread0 = executor.submit(self.__getDailyGamesUrls__, soup)
            thread1 = executor.submit(self.__getDailyGamesImages__, soup)
            thread2 = executor.submit(self.__getDailyGamesOriginalPrice__, soup)
            thread3 = executor.submit(self.__getDailyGamesFinalPrice__, soup)
            

        urls           = thread0.result()
        images         = thread1.result()
        originalPrices = thread2.result()
        finalPrices    = thread3.result()

        return urls, images, originalPrices, finalPrices

    def __getDailyGamesUrls__(self, soup: BeautifulSoup):
        urls = []

        for dailyGames in soup.find_all('div', class_='dailydeal_cap'):
            urls.append(dailyGames.contents[1].attrs['href'])

        return urls

    def __getDailyGamesImages__(self, soup: BeautifulSoup):
        images = []

        for dailyGames in soup.find_all('div', class_='dailydeal_cap'):
            images.append(dailyGames.contents[1].contents[1].attrs['src'])

        return images

    def __getDailyGamesOriginalPrice__(self, soup: BeautifulSoup):
        originalPrice = []

        for dailyGames in soup.find_all('div', class_='dailydeal_ctn'):
            dailyGamesPrices = dailyGames.find_all('div', class_='discount_prices')
            temp = str(dailyGamesPrices).split('>')
            
            # Caso não tenha nenhum preço para o jogo.
            try:
                temp1 = temp[2].split('</div')
            except:
                temp1 = ["Não disponível!"]

            originalPrice.append(temp1[0])

        return originalPrice

    def __getDailyGamesFinalPrice__(self, soup: BeautifulSoup):
        finalPrice = []

        for dailyGames in soup.find_all('div', class_='dailydeal_ctn'):
            dailyGamesPrices = dailyGames.find_all('div', class_='discount_prices')
            temp = str(dailyGamesPrices).split('>')
            # Caso não tenha nenhum preço para o jogo.
            try:
                temp1 = temp[4].split('</div')
            except:
                temp1 = ["Não disponível!"]

            finalPrice.append(temp1[0])

        return finalPrice

    # Função que retorna três listas, uma contendo a URL, outra contendo as imagens,
    # e por fim, outra contendo a descrição do evento/jogo em destaque.
    async def getSpotlightOffers(self):
        soup = self.reqUrl(URL_SPECIALS)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            thread0 = executor.submit(self.__getSpotlightUrls__, soup)
            thread1 = executor.submit(self.__getSpotlightImages__, soup)
            thread2 = executor.submit(self.__getSpotlightContents__, soup)

        urls     = thread0.result()
        images   = thread1.result()
        contents = thread2.result()

        return urls, images, contents
    
    def __getSpotlightUrls__(self, soup: BeautifulSoup):
        urls = []

        for spotlightGames in soup.find_all('div', class_='spotlight_img'):
            urls.append(spotlightGames.contents[1].attrs['href'])

        return urls

    def __getSpotlightImages__(self, soup: BeautifulSoup):
        images = []

        for spotlightGames in soup.find_all('div', class_='spotlight_img'):
            images.append(spotlightGames.contents[1].contents[1].attrs['src'])

        return images

    def __getSpotlightContents__(self, soup: BeautifulSoup):
        contents = []

        for spotlightGames in soup.find_all('div', class_='spotlight_content'):
            contents.append(spotlightGames.contents[1].contents[0])

        return contents

    # Função que retorna cinco listas que possuem respectivamente as seguintes
    # informações: nome, URL, preço original, preço com desconto e imagens; 
    # dos jogos/DLCs de uma categoria.
    async def getTabContent(self, url: str, divId: str):
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

    #Função que retorna o nome, o preço, a url e a imagem de um jogo específico.
    async def getSpecificGame(self, gameName: str):
        searchUrl = URL_GAME + gameName
        soup = self.reqUrl(searchUrl)

        try:
            game         = soup.find(id='search_resultsRows').find(class_='search_result_row ds_collapse_flag')
            haveDiscount = True if len(game.find(class_='search_price').contents) > 1 else False

            with concurrent.futures.ThreadPoolExecutor() as executor:
                thread0 = executor.submit(self.__getSpecifcGameUrl__, game)
                thread1 = executor.submit(self.__getSpecifcGameImage__, game)
                thread2 = executor.submit(self.__getSpecifcGameName__, game)
                thread3 = executor.submit(self.__getSpecifcGameOriginalPrice__, game, haveDiscount)
                thread4 = executor.submit(self.__getSpecifcGameFinalPrice__, game, haveDiscount)

            url          = thread0.result()
            image        = thread1.result()
            name         = thread2.result()
            orginalPrice = thread3.result()
            finalPrice   = thread4.result()
        except:
            url = image = name = orginalPrice = orginalPrice = None

        return name, url, image, orginalPrice, finalPrice, searchUrl.replace(" ", "%20")

    def __getSpecifcGameUrl__(self, game: BeautifulSoup):
        return game.attrs['href']

    def __getSpecifcGameImage__(self, game: BeautifulSoup):
        return game.find('img').attrs['srcset'].split(" ")[2]

    def __getSpecifcGameName__(self, game: BeautifulSoup):
        return game.find(class_='search_name').contents[1].contents[0]

    def __getSpecifcGameOriginalPrice__(self, game: BeautifulSoup, haveDiscount: bool):
        if(haveDiscount):
            return game.find(class_='search_price').contents[1].contents[0].contents[0]
        else:
            temp = sub(r"\s+", "" , game.find(class_='search_price').contents[0])
            
            if(not temp.isnumeric()):
                return "Não disponível!"
            
            if(temp.find('Gratuito') != -1):
                temp = "Gratuiro p/ Jogar"

            return temp

    def __getSpecifcGameFinalPrice__(self, game: BeautifulSoup, haveDiscount: bool):
        if(haveDiscount):
            temp = sub(r"\s+", "" , game.find(class_='search_price').contents[3])

            return temp
        else:
            temp = sub(r"\s+", "" , game.find(class_='search_price').contents[0])

            if(not temp.isnumeric()):
                return "Não disponível!"
            
            if(temp.find('Gratuito') != -1):
                temp = "Gratuiro p/ Jogar"

            return temp


    # Função que retorna um jogo recomendado de um gênero específico.
    async def getGameRecommendationByGenre(self, genre: str):
        # Convertendo para lower case
        genre = genre.lower()

        if(genre == 'acao'):
            genre = 'ação'
        elif(genre == 'estrategia'):
            genre = 'estratégia'
        elif(
            genre == 'multijogador massivo'
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
    async def getGameRecommendationByPriceRange(self, maxPrice: str):
        if(maxPrice == "rZ04j"):
            url           = URL_PRICE_RANGE
            maxPriceFloat = None
        elif(maxPrice == "19Jfc"):
            url           = URL_PRICE_RANGE + '&maxprice=10&cc=br'
            maxPriceFloat = 10.0
        else:
            url           = URL_PRICE_RANGE + '&maxprice={}&cc=br'.format(maxPrice)
            maxPriceFloat = float(maxPrice)
        
        soup             = self.reqUrl(url)
        gameNames        = []
        gameImages       = []
        gameUrls         = []
        gameOrinalPrices = []
        gameFinalPrices  = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
                thread0 = executor.submit(self.__getRecommendationByPriceRangeNames__, soup)
                thread1 = executor.submit(self.__getRecommendationByPriceRangeImages__, soup)
                thread2 = executor.submit(self.__getRecommendationByPriceRangeOriginalPrices__, soup)
                thread3 = executor.submit(self.__getRecommendationByPriceRangeFinalPrices__, soup)
                thread4 = executor.submit(self.__getRecommendationByPriceRangeUrls__, soup)

        gameNames        = thread0.result()
        gameImages       = thread1.result()
        gameOrinalPrices = thread2.result()
        gameFinalPrices  = thread3.result()
        gameUrls        = thread4.result()

        number = randint(0, len(gameNames) - 1)

        # Verificando se o jogo está na faixa de preço indicada.
        # Isso é necessário, pois em alguns casos, mesmo definindo a faixa, a
        # Steam deixa passar alguns jogos.
        if(
            gameFinalPrices[number] != "Gratuito para jogar" or 
            gameFinalPrices[number] != "Não disponível!"
        ):
            if(maxPriceFloat != None):
                while(True):
                    temp = gameFinalPrices[number]

                    if(
                        temp == "Gratuito para jogar" or 
                        temp == "Não disponível!"
                    ):
                        break

                    temp1      = temp.split("R$")[1]
                    finalPrice = float(temp1.replace(",", "."))
                    
                    if(finalPrice < maxPriceFloat):
                        break
                    
                    number = randint(0, len(gameNames) - 1)
                    

        gameName        = gameNames[number]
        gameImage       = gameImages[number]
        gameUrl         = gameUrls[number]
        gameOrinalPrice = gameOrinalPrices[number]
        gameFinalPrice  = gameFinalPrices[number]

        return gameName, gameImage, gameUrl, gameOrinalPrice, gameFinalPrice

    def __getRecommendationByPriceRangeNames__(self, soup: BeautifulSoup):
        names = []

        for listDivGamesNames in soup.find_all('div', class_="search_name"):
            for listSpanGamesNames in listDivGamesNames.find_all('span', class_="title"):
                names.append(listSpanGamesNames.contents[0])

        return names

    def __getRecommendationByPriceRangeImages__(self, soup: BeautifulSoup):
        images = []

        for listDivGamesImages in soup.find_all('div', class_="search_capsule"):
            for listImgGamesImages in listDivGamesImages.find_all('img'):
                img = listImgGamesImages.attrs['srcset'].split(" ")[2]
                images.append(img)

        return images

    def __getRecommendationByPriceRangeOriginalPrices__(self, soup: BeautifulSoup):
        originalPrices = []

        for listDivGamesPrices in soup.find_all('div', class_='search_price'):
            if(listDivGamesPrices.contents[0] == '\n'):
                if(len(listDivGamesPrices.contents) == 4):
                    
                    for listSpanGamesPrices in listDivGamesPrices.find_all('span'):
                        originalPrices.append(listSpanGamesPrices.contents[0].contents[0])
                else:
                    originalPrices.append("Não disponível!")
            else:
                temp = sub(r"\s+", "" , listDivGamesPrices.contents[0])

                if(temp == "Gratuitoparajogar" or temp == "Gratuitop/Jogar"):
                    temp = "Gratuito para jogar"
                    
                originalPrices.append(temp)

        return originalPrices

    def __getRecommendationByPriceRangeFinalPrices__(self, soup: BeautifulSoup):
        finalPrices = []

        for listDivGamesPrices in soup.find_all('div', class_='search_price'):
            if(listDivGamesPrices.contents[0] == '\n'):
                if(len(listDivGamesPrices.contents) == 4):
                    temp = sub(r"\s+", "" , listDivGamesPrices.contents[3])
                    finalPrices.append(temp)
                else:
                    finalPrices.append("Não disponível!")
            else:
                temp = sub(r"\s+", "" , listDivGamesPrices.contents[0])

                if(temp == "Gratuitoparajogar" or temp == "Gratuitop/Jogar"):
                    temp = "Gratuito para jogar"
                    
                finalPrices.append(temp)

        return finalPrices

    def __getRecommendationByPriceRangeUrls__(self, soup: BeautifulSoup):
        urls = []

        for listAGamesUrls in soup.find_all('a', class_="search_result_row"):
            urls.append(listAGamesUrls.attrs['href'])

        return urls