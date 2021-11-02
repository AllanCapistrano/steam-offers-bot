from random import randint
import concurrent.futures
import requests
from bs4 import BeautifulSoup

from services.tabContent import TabContent
from services.tabContentRow import TabContentRow
from services.genreFormatting import genreFormatting

from services.DailyGames.getDailyGamesUrls import getDailyGamesUrls
from services.DailyGames.getDailyGamesImages import getDailyGamesImages
from services.DailyGames.getDailyGamesOriginalPrice import getDailyGamesOriginalPrice
from services.DailyGames.getDailyGamesFinalPrice import getDailyGamesFinalPrice

from services.SpotlightOffers.getSpotlightUrls import getSpotlightUrls
from services.SpotlightOffers.getSpotlightImages import getSpotlightImages
from services.SpotlightOffers.getSpotlightContents import getSpotlightContents

from services.TabContent.getTabContentNames import getTabContentNames
from services.TabContent.getTabContentUrls import getTabContentUrls
from services.TabContent.getTabContentHasPrice import getTabContentHasPrice
from services.TabContent.getTabContentOriginalPrices import getTabContentOriginalPrices
from services.TabContent.getTabContentFinalPrices import getTabContentFinalPrices
from services.TabContent.getTabContentImages import getTabContentImages

from services.SpecificGame.getSpecificGameUrl import getSpecificGameUrl
from services.SpecificGame.getSpecificGameImage import getSpecificGameImage
from services.SpecificGame.getSpecificGameName import getSpecificGameName
from services.SpecificGame.getSpecificGameOriginalPrice import getSpecificGameOriginalPrice
from services.SpecificGame.getSpecificGameFinalPrice import getSpecificGameFinalPrice

from services.RecommendationByPriceRange.getRecommendationByPriceRangeNames import getRecommendationByPriceRangeNames
from services.RecommendationByPriceRange.getRecommendationByPriceRangeImages import getRecommendationByPriceRangeImages
from services.RecommendationByPriceRange.getRecommendationByPriceRangeOriginalPrices import getRecommendationByPriceRangeOriginalPrices
from services.RecommendationByPriceRange.getRecommendationByPriceRangeFinalPrices import getRecommendationByPriceRangeFinalPrices
from services.RecommendationByPriceRange.getRecommendationByPriceRangeUrls import getRecommendationByPriceRangeUrls
from services.RecommendationByPriceRange.verifyPriceRange import verifyPriceRange

from services.GameByLink.getGameByLinkName import getGameByLinkName
from services.GameByLink.getGameByLinkImage import getGameByLinkImage
from services.GameByLink.getGameByLinkOriginalPrice import getGameByLinkOriginalPrice
from services.GameByLink.getGameByLinkFinalPrice import getGameByLinkFinalPrice

# ------------------------------ Constants ----------------------------------- #
URL_MAIN = 'https://store.steampowered.com/?cc=br&l=brazilian'
URL_SPECIALS = 'https://store.steampowered.com/specials?cc=br&l=brazilian'
URL_GAME = 'https://store.steampowered.com/search/?cc=br&l=brazilian&term='
URL_GENRE = 'https://store.steampowered.com/category/'
URL_PRICE_RANGE = 'https://store.steampowered.com/search/?l=brazilian'
# ---------------------------------------------------------------------------- #
class Crawler:
    # ------------------------#- Request Url --------------------------------- #
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
    # ------------------------------------------------------------------------ #

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
            thread0 = executor.submit(getDailyGamesUrls, soup)
            thread1 = executor.submit(getDailyGamesImages, soup)
            thread2 = executor.submit(getDailyGamesOriginalPrice, soup)
            thread3 = executor.submit(getDailyGamesFinalPrice, soup)
            

        urls           = thread0.result()
        images         = thread1.result()
        originalPrices = thread2.result()
        finalPrices    = thread3.result()

        return urls, images, originalPrices, finalPrices
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
            thread0 = executor.submit(getSpotlightUrls, soup)
            thread1 = executor.submit(getSpotlightImages, soup)
            thread2 = executor.submit(getSpotlightContents, soup)

        urls     = thread0.result()
        images   = thread1.result()
        contents = thread2.result()

        # Verificação se todos os destaque possuem descrição.
        if(len(urls) != len(contents)):
            noMatches = []

            for i in range(0, len(urls)):
                for j in range(0, len(contents)):
                    if(urls[i]["id"] == contents[j]["id"]):
                        break
                    # Somente quando não foi encontrado.
                    if(j == len(contents) - 1):
                        noMatches.append(i)

            for index in noMatches:
                tempDict = {
                    "id": urls[index]["id"],
                    "value": "Indisponível"
                }

                contents.insert(index, tempDict)

        return urls, images, contents
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
                thread0 = executor.submit(getTabContentNames, tabContent)
                thread1 = executor.submit(getTabContentUrls, tabContent)
                thread2 = executor.submit(getTabContentHasPrice, tabContent)
                thread3 = executor.submit(getTabContentOriginalPrices, tabContent)
                thread4 = executor.submit(getTabContentFinalPrices, tabContent)
                thread5 = executor.submit(getTabContentImages, tabContent)
                
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
                thread0 = executor.submit(getSpecificGameUrl, game)
                thread1 = executor.submit(getSpecificGameImage, game)
                thread2 = executor.submit(getSpecificGameName, game)
                thread3 = executor.submit(getSpecificGameOriginalPrice, game, haveDiscount)
                thread4 = executor.submit(getSpecificGameFinalPrice, game, haveDiscount)

            url          = thread0.result()
            image        = thread1.result()
            name         = thread2.result()
            orginalPrice = thread3.result()
            finalPrice   = thread4.result()
        except:
            url = image = name = orginalPrice = finalPrice = None

        return name, url, image, orginalPrice, finalPrice, searchUrl.replace(" ", "%20")
    # ------------------------------------------------------------------------ #

    # ---------------------- Recommendation By Genre ------------------------- #
    async def getGameRecommendationByGenre(self, genre: str) -> tuple[list, list, list, list, list]:
        """Função responsável por recomendar um jogo com base em gênero 
        especificado.

        Parameters
        -----------
        genre: :class:`str`
            Gênero do jogo.

        Returns
        -----------
        gameName: :class:`list`
            Nome do jogo.
        gameUrl: :class:`list`
            Url do jogo.
        gameOriginalPrice: :class:`list`
            Preço original do jogo.
        gameFinalPrice: :class:`list`
            Preço com desconto do jogo.
        gameImage: :class:`list`
            Imagem do jogo.
        """
        
        genre = genreFormatting(genre)

        pos           = randint(0, len(TabContent) - 1)
        tabContent    = TabContent(pos).name
        tabContentRow = TabContentRow(pos).name
        url           = URL_GENRE + '{}/?l=brazilian&cc=br#p=0&tab={}'.format(genre, tabContent)

        try:
            (
                gamesNames, 
                gamesUrls, 
                gamesOriginalPrices, 
                gamesFinalPrices, 
                gamesImages
            ) = await self.getTabContent(url, tabContentRow)
            
            index            = randint(0, len(gamesNames) - 1)
            gameName          = gamesNames[index]
            gameUrl           = gamesUrls[index]
            gameOriginalPrice = gamesOriginalPrices[index]
            gameFinalPrice    = gamesFinalPrices[index]
            gameImage         = gamesImages[index]
        except:
            gameName = gameUrl = gameOriginalPrice = gameFinalPrice = gameImage = None

        return gameName, gameUrl, gameOriginalPrice, gameFinalPrice, gameImage
    # ------------------------------------------------------------------------ #

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
                thread0 = executor.submit(getRecommendationByPriceRangeNames, soup)
                thread1 = executor.submit(getRecommendationByPriceRangeImages, soup)
                thread2 = executor.submit(getRecommendationByPriceRangeOriginalPrices, soup)
                thread3 = executor.submit(getRecommendationByPriceRangeFinalPrices, soup)
                thread4 = executor.submit(getRecommendationByPriceRangeUrls, soup)
                
        gameNames        = thread0.result()
        gameImages       = thread1.result()
        gameOrinalPrices = thread2.result()
        gameFinalPrices  = thread3.result()
        gameUrls         = thread4.result()

        index = verifyPriceRange(maxPriceFloat, gameFinalPrices)

        gameName        = gameNames[index]
        gameImage       = gameImages[index]
        gameUrl         = gameUrls[index]
        gameOrinalPrice = gameOrinalPrices[index]
        gameFinalPrice  = gameFinalPrices[index]

        return gameName, gameImage, gameUrl, gameOrinalPrice, gameFinalPrice
    # ------------------------------------------------------------------------ #

    # ------------------------- Game By Link --------------------------------- #
    async def getGameByLink(self, url: str) -> tuple[str, str, str, str]:
        """Função responsável por retornar um jogo com base no link enviado.

        Parameters
        -----------
        url: :class:`str`
            URL do jogo enviada.

        Returns
        -----------
        name: :class:`str`
            Nome do jogo.
        image: :class:`str`
            Imagem do jogo.
        orginalPrice: :class:`str`
            Preço original do jogo.
        finalPrice: :class:`str`
            Preço com desconto do jogo.
        """
        
        soup = self.reqUrl(url + "?cc=br&l=brazilian")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            thread0 = executor.submit(getGameByLinkName, soup)
            thread1 = executor.submit(getGameByLinkImage, soup)
            thread2 = executor.submit(getGameByLinkOriginalPrice, soup)
            thread3 = executor.submit(getGameByLinkFinalPrice, soup)

        name          = thread0.result()
        image         = thread1.result()
        orginalPrice  = thread2.result()
        finalPrice    = thread3.result()

        return name, image, orginalPrice, finalPrice
    # ------------------------------------------------------------------------ #