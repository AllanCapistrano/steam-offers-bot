from re import sub
from random import randint
import concurrent.futures
import requests
from bs4 import BeautifulSoup

from myUtils.tabContent import TabContent
from myUtils.tabContentRow import TabContentRow

# -------------------------- Constants ----------------------------------- #
URL_MAIN = 'https://store.steampowered.com/?cc=br&l=brazilian'
URL_SPECIALS = 'https://store.steampowered.com/specials?cc=br&l=brazilian'
URL_GAME = 'https://store.steampowered.com/search/?cc=br&l=brazilian&term='
URL_GENRE = 'https://store.steampowered.com/tags/pt-br/'
URL_PRICE_RANGE = 'https://store.steampowered.com/search/?l=brazilian'
# ------------------------------------------------------------------------ #
class CatchOffers:
    def reqUrl(self, url: str) -> BeautifulSoup:
        """ Função responsável por buscar as Urls.

        Parameters
        -----------
        url: :class:`str`
            Url do site.

        Returns
        -----------
        soup: :class:`BeautifulSoup`
        """

        r    = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        
        return soup

    # -------------------------- Daily Games --------------------------------- #
    async def getDailyGamesOffers(self) -> tuple[list, list, list, list]:
        """Função responsável por retornar as informações dos jogos que estão
        em promoção.

        Returns
        -----------
        urls: :class:`list`
            Lista com as urls dos jogos.
        images: :class:`list`
            Lista com as imagens dos jogos.
        originalPrices: :class:`list`
            Lista com os preços originais dos jogos.
        finalPrices: :class:`list`
            Lista com os preços com o desconto aplicado dos jogos.
        """
        
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

    def __getDailyGamesUrls__(self, soup: BeautifulSoup) -> list:
        """ Função responsável por retornar uma lista contendo as urls dos jogos
        que estão em promoção.

        Parameters
        -----------
        soup: :class:`BeautifulSoup`

        Returns
        -----------
        urls: :class:`list`
        """

        urls = []

        for dailyGames in soup.find_all('div', class_='dailydeal_cap'):
            urls.append(dailyGames.contents[1].attrs['href'])

        return urls

    def __getDailyGamesImages__(self, soup: BeautifulSoup) -> list:
        """ Função responsável por retornar uma lista contendo as imagens dos 
        jogos que estão em promoção.

        Parameters
        -----------
        soup: :class:`BeautifulSoup`

        Returns
        -----------
        images: :class:`list`
        """
        
        images = []

        for dailyGames in soup.find_all('div', class_='dailydeal_cap'):
            images.append(dailyGames.contents[1].contents[1].attrs['src'])

        return images

    def __getDailyGamesOriginalPrice__(self, soup: BeautifulSoup) -> list:
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

    def __getDailyGamesFinalPrice__(self, soup: BeautifulSoup) -> list:
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
    # ------------------------------------------------------------------------ #

    # -------------------------- Spotlight ----------------------------------- #
    async def getSpotlightOffers(self) -> tuple[list, list, list]:
        """Função responsável por retornar as informações dos jogos que estão
        em destaque.

        Returns
        -----------
        urls: :class:`list`
            Lista com as urls dos jogos.
        images: :class:`list`
            Lista com as imagens dos jogos.
        contents: :class:`list`
            Lista contento as informações dos jogos.
        """
        
        soup = self.reqUrl(URL_SPECIALS)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            thread0 = executor.submit(self.__getSpotlightUrls__, soup)
            thread1 = executor.submit(self.__getSpotlightImages__, soup)
            thread2 = executor.submit(self.__getSpotlightContents__, soup)

        urls     = thread0.result()
        images   = thread1.result()
        contents = thread2.result()

        return urls, images, contents
    
    def __getSpotlightUrls__(self, soup: BeautifulSoup) -> list:
        """ Função responsável por retornar uma lista contendo as urls dos jogos
        que estão em destaque.

        Parameters
        -----------
        soup: :class:`BeautifulSoup`

        Returns
        -----------
        urls: :class:`list`
        """

        urls = []

        for spotlightGames in soup.find_all('div', class_='spotlight_img'):
            urls.append(spotlightGames.contents[1].attrs['href'])

        return urls

    def __getSpotlightImages__(self, soup: BeautifulSoup) -> list:
        """ Função responsável por retornar uma lista contendo as imagens dos 
        jogos que estão em destaque.

        Parameters
        -----------
        soup: :class:`BeautifulSoup`

        Returns
        -----------
        images: :class:`list`
        """
        
        images = []

        for spotlightGames in soup.find_all('div', class_='spotlight_img'):
            images.append(spotlightGames.contents[1].contents[1].attrs['src'])

        return images

    def __getSpotlightContents__(self, soup: BeautifulSoup) -> list:
        """ Função responsável por retornar uma lista contendo as informações dos 
        jogos que estão em destaque.

        Parameters
        -----------
        soup: :class:`BeautifulSoup`

        Returns
        -----------
        contents: :class:`list`
        """
        
        contents = []

        for spotlightGames in soup.find_all('div', class_='spotlight_content'):
            contents.append(spotlightGames.contents[1].contents[0])

        return contents
    # ------------------------------------------------------------------------ #

    # ------------------------- Tab Content ---------------------------------- #
    async def getTabContent(self, url: str, divId: str) -> tuple[list, list, list, list, list]:
        """Função responsável por retornar as informações dos jogos que estão
        em uma aba específica.

        Parameters
        -----------
        url: :class:`str`
        divId: :class:`str`

        Returns
        -----------
        names: :class:`list`
            Lista com os nomes dos jogos.
        urls: :class:`list`
            Lista com as urls dos jogos.
        originalPrices: :class:`list`
            Lista com os preços originais dos jogos.
        finalPrices: :class:`list`
            Lista com os preços com o desconto aplicado dos jogos.
        images: :class:`list`
            Lista com as imagens dos jogos.
        """
        
        soup = self.reqUrl(url)

        for tabContent in soup.find_all('div', id=divId):
            with concurrent.futures.ThreadPoolExecutor() as executor:
                thread0 = executor.submit(self.__getTabContentNames__, tabContent)
                thread1 = executor.submit(self.__getTabContentUrls__, tabContent)
                thread2 = executor.submit(self.__getTabContentHasPrice__, tabContent)
                thread3 = executor.submit(self.__getTabContentOriginalPrices__, tabContent)
                thread4 = executor.submit(self.__getTabContentFinalPrices__, tabContent)
                thread5 = executor.submit(self.__getTabContentImages__, tabContent)

            names                          = thread0.result()
            urls                           = thread1.result()
            (hasPrice, gameWithoutPricing) = thread2.result()
            originalPrices                 = thread3.result()
            finalPrices                    = thread4.result()
            images                         = thread5.result()

        # Verifica se há pelo menos um jogo sem preço. Em caso afirmativo, 
        # adiciona essa infomação na posição correta da lista.
        if(gameWithoutPricing):
            for x in range(len(hasPrice) - 1):
                if(not hasPrice[x]):
                    originalPrices.insert(x, 'Preço indisponível!')
                    finalPrices.insert(x, 'Preço indisponível!')

        return names, urls, originalPrices, finalPrices, images

    def __getTabContentNames__(self, soup: BeautifulSoup) -> list:
        """ Função responsável por retornar uma lista contendo os nomes dos jogos
        que estão em uma aba específica.

        Parameters
        -----------
        soup: :class:`BeautifulSoup`

        Returns
        -----------
        names: :class:`list`
        """
        
        names = []

        for tabContent in soup.find_all('div', class_='tab_item_name'):
            names.append(tabContent.contents[0])

        return names
    
    def __getTabContentUrls__(self, soup: BeautifulSoup) -> list:
        """ Função responsável por retornar uma lista contendo as urls dos jogos
        que estão em uma aba específica.

        Parameters
        -----------
        soup: :class:`BeautifulSoup`

        Returns
        -----------
        urls: :class:`list`
        """
        
        urls = []

        for tabContent in soup.find_all('a', class_='tab_item'):
            urls.append(tabContent.attrs['href'])

        return urls
    
    def __getTabContentHasPrice__(self, soup: BeautifulSoup) -> tuple[list, bool]:
        """ Função responsável por retornar uma lista que indica a posição dos
        jogos que não possuem nenhuma precificação (caso exista).

        Parameters
        -----------
        soup: :class:`BeautifulSoup`

        Returns
        -----------
        hasPrice: :class:`list`
        gameWithoutPricing: :class:`bool`
        """
        
        hasPrice           = []
        gameWithoutPricing = False

        for tabContent in soup.find_all('div', class_='discount_block'):
            try:
                tabContent['class'].index("empty")
                hasPrice.append(False)
                
                gameWithoutPricing = True
            except:
                hasPrice.append(True)

        return hasPrice, gameWithoutPricing
    
    def __getTabContentOriginalPrices__(self, soup: BeautifulSoup) -> list:
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

    def __getTabContentFinalPrices__(self, soup: BeautifulSoup) ->list:
        """ Função responsável por retornar uma lista contendo os preços dos 
        jogos com o desconto aplicado, que estão em uma aba específica.

        Parameters
        -----------
        soup: :class:`BeautifulSoup`

        Returns
        -----------
        finalPrices: :class:`list`
        """
        
        finalPrices = []

        for tabContent in soup.find_all('div', class_='discount_prices'):                
            if(len(tabContent) == 2):
                finalPrices.append(tabContent.contents[1].contents[0])
            elif(len(tabContent) == 1):
                temp = tabContent.contents[0].contents[0]

                if(temp.find('Free') != -1):
                    temp = "Gratuiro p/ Jogar"

                finalPrices.append(temp)

        return finalPrices

    def __getTabContentImages__(self, soup: BeautifulSoup) -> list:
        """ Função responsável por retornar uma lista contendo as imagens dos
        jogos que estão em uma aba específica.

        Parameters
        -----------
        soup: :class:`BeautifulSoup`

        Returns
        -----------
        images: :class:`list`
        """
        
        images = []

        for tabContent in soup.find_all('img', class_='tab_item_cap_img'):
            # Alterando a resolução da imagem.
            imgResized = tabContent.attrs['src'].replace("184x69", "231x87")

            images.append(imgResized)

        return images
    # ------------------------------------------------------------------------ #

    # ------------------------ Specific Game --------------------------------- #
    async def getSpecificGame(self, gameName: str) -> tuple[str, str, str, str, str, str]:
        """Função responsável por retornar as informações e um jogo específico.

        Parameters
        -----------
        gameName: :class:`str`
            Nome do jogo que se deseja obter informações.

        Returns
        -----------
        name: :class:`str`
            Nome do jogo.
        url: :class:`str`
            Url do jogo.
        image: :class:`str`
            Imagem do jogo.
        orginalPrice: :class:`str`
            Preço original do jogo.
        finalPrice: :class:`str`
            Preço com desconto do jogo.
        searchUrl: :class:`str`
            Url de busca do jogo, caso o jogo especificado não seja o encontrado.
        """
        
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

    def __getSpecifcGameUrl__(self, game: BeautifulSoup) -> str:
        """ Função responsável a url do jogo.

        Parameters
        -----------
        game: :class:`BeautifulSoup`

        Returns
        -----------
        url: :class:`str`
        """
        
        return game.attrs['href']

    def __getSpecifcGameImage__(self, game: BeautifulSoup) -> str:
        """ Função responsável a imagem do jogo.

        Parameters
        -----------
        game: :class:`BeautifulSoup`

        Returns
        -----------
        image: :class:`str`
        """
        
        return game.find('img').attrs['srcset'].split(" ")[2]

    def __getSpecifcGameName__(self, game: BeautifulSoup) -> str:
        """ Função responsável por retornar o nome do jogo como está na Steam.

        Parameters
        -----------
        game: :class:`BeautifulSoup`

        Returns
        -----------
        name: :class:`str`
        """
        
        return game.find(class_='search_name').contents[1].contents[0]

    def __getSpecifcGameOriginalPrice__(self, game: BeautifulSoup, haveDiscount: bool) -> str:
        """ Função responsável o preço original do jogo.

        Parameters
        -----------
        game: :class:`BeautifulSoup`,
        haveDiscount :class:`bool`

        Returns
        -----------
        url: :class:`str`
        """
        
        if(haveDiscount):
            return game.find(class_='search_price').contents[1].contents[0].contents[0]
        else:
            temp = sub(r"\s+", "" , game.find(class_='search_price').contents[0])
            
            if(not temp.isnumeric()):
                return "Não disponível!"
            
            if(temp.find('Gratuito') != -1):
                temp = "Gratuiro p/ Jogar"

            return temp

    def __getSpecifcGameFinalPrice__(self, game: BeautifulSoup, haveDiscount: bool) -> str:
        """ Função responsável o preço com desconto do jogo.

        Parameters
        -----------
        game: :class:`BeautifulSoup`,
        haveDiscount :class:`bool`

        Returns
        -----------
        url: :class:`str`
        """
        
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
    # ------------------------------------------------------------------------ #

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

    # ----------------- Recommendation By Price Range ------------------------ #
    async def getGameRecommendationByPriceRange(self, maxPrice: str) -> tuple[str, str, str, str, str]:
        """Função que retorna um jogo com base numa faixa de preço especificada.

        Parameters
        -----------
        maxPrice: :class:`str`
            Faixa de preço.

        Returns
        -----------
        gameName: :class:`str`
            Nome do jogo.
        gameImage: :class:`str`
            Imagem do jogo.
        gameUrl: :class:`str`
            Url do jogo.
        gameOrinalPrice: :class:`str`
            Preço original do jogo.
        gameFinalPrice: :class:`str`
            Preço com desconto do jogo.
        """
        
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

    def __getRecommendationByPriceRangeNames__(self, soup: BeautifulSoup) -> list:
        """ Função responsável por retornar uma lista contendo os nomes dos jogos
        que estão na faixa de preço especificada.

        Parameters
        -----------
        soup: :class:`BeautifulSoup`

        Returns
        -----------
        names: :class:`list`
        """
        
        names = []

        for listDivGamesNames in soup.find_all('div', class_="search_name"):
            for listSpanGamesNames in listDivGamesNames.find_all('span', class_="title"):
                names.append(listSpanGamesNames.contents[0])

        return names

    def __getRecommendationByPriceRangeImages__(self, soup: BeautifulSoup) -> list:
        """ Função responsável por retornar uma lista contendo as imagens dos 
        jogos que estão na faixa de preço especificada.

        Parameters
        -----------
        soup: :class:`BeautifulSoup`

        Returns
        -----------
        images: :class:`list`
        """
        
        images = []

        for listDivGamesImages in soup.find_all('div', class_="search_capsule"):
            for listImgGamesImages in listDivGamesImages.find_all('img'):
                img = listImgGamesImages.attrs['srcset'].split(" ")[2]
                images.append(img)

        return images

    def __getRecommendationByPriceRangeOriginalPrices__(self, soup: BeautifulSoup) -> list:
        """ Função responsável por retornar uma lista contendo os preços originais 
        dos jogos que estão na faixa de preço especificada.

        Parameters
        -----------
        soup: :class:`BeautifulSoup`

        Returns
        -----------
        originalPrices: :class:`list`
        """
        
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

    def __getRecommendationByPriceRangeFinalPrices__(self, soup: BeautifulSoup) -> list:
        """ Função responsável por retornar uma lista contendo os preços com 
        desconto dos jogos que estão na faixa de preço especificada.

        Parameters
        -----------
        soup: :class:`BeautifulSoup`

        Returns
        -----------
        finalPrices: :class:`list`
        """
        
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

    def __getRecommendationByPriceRangeUrls__(self, soup: BeautifulSoup) -> list:
        """ Função responsável por retornar uma lista contendo as urls dos jogos 
        que estão na faixa de preço especificada.

        Parameters
        -----------
        soup: :class:`BeautifulSoup`

        Returns
        -----------
        urls: :class:`list`
        """
        
        urls = []

        for listAGamesUrls in soup.find_all('a', class_="search_result_row"):
            urls.append(listAGamesUrls.attrs['href'])

        return urls
    # ------------------------------------------------------------------------ #