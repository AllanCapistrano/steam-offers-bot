from random import randint
import concurrent.futures
import requests
from bs4 import BeautifulSoup

from services.tabContent import TabContent
from services.tabContentRow import TabContentRow
from services.genreFormatting import genreFormatting
from services.handlePriceIssues import handlePriceIssues

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

from services.GameReview.getReviewTotalAmount import getReviewTotalAmount
from services.GameReview.getReviewSumary import getReviewSumary

# ------------------------------ Constants ----------------------------------- #
URL_MAIN = "https://store.steampowered.com/?cc=br&l=brazilian"
URL_SPECIALS = "https://store.steampowered.com/specials?"
URL_GAME = "https://store.steampowered.com/search/?"
URL_GENRE = "https://store.steampowered.com/category/"
URL_PRICE_RANGE = "https://store.steampowered.com/search/?"
# ---------------------------------------------------------------------------- #
class Crawler:
    # -------------------------- Request Url --------------------------------- #
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

    # -------------------------- Request Url --------------------------------- #
    def getGameDescription(self, soup: BeautifulSoup) -> str:
        """ Função responsável por retornar a descrição do jogo.

        Parameters
        -----------
        soup: :class:`BeautifulSoup`,

        Returns
        -----------
        description: :class:`str`
        """

        try:
            temp = soup.find(class_="game_description_snippet").contents[0].strip()
        except:
            temp = None

        return temp
    # ------------------------------------------------------------------------ #

    # -------------------------- Daily Games --------------------------------- #
    async def getDailyGamesOffers(
        self,
        currency: str,
        language: str
    ) -> tuple[list, list, list, list]:
        """Função responsável por retornar as informações dos jogos que estão
        em promoção.

        Parameters
        -----------
        currency: :class:`str`
            Moeda que se deseja ver o preço.
        language: :class:`str`
            Linguagem que se deseja visualizar a página do jogo. 

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
        
        soup = self.reqUrl(f"{URL_SPECIALS}cc={currency}&l={language}")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            thread0 = executor.submit(getDailyGamesUrls, soup)
            thread1 = executor.submit(getDailyGamesImages, soup)
            thread2 = executor.submit(getDailyGamesOriginalPrice, soup)
            thread3 = executor.submit(getDailyGamesFinalPrice, soup)
            
        urls   = thread0.result()
        images = thread1.result()

        # Verificação de incoerências nos preços.
        (
            originalPrices, 
            finalPrices
        ) = handlePriceIssues(
                originalPrices=thread2.result(), 
                finalPrices=thread3.result()
            )

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
        
        # Rever linguagem daqui
        soup = self.reqUrl(f"{URL_SPECIALS}cc=br&l=brazilian")

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
    async def getTabContent(
        self, 
        url: str, 
        divId: str,
        language: str = None
    ) -> tuple[list, list, list, list, list]:
        """Função responsável por retornar as informações dos jogos que estão
        em uma aba específica.

        Parameters
        -----------
        url: :class:`str`
        divId: :class:`str`
        language: :class:`str`

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
                    if(language == None):
                        originalPrices.insert(x, 'Preço indisponível!')
                        finalPrices.insert(x, 'Preço indisponível!')
                    elif(language == "english"):
                        originalPrices.insert(x, 'Not available!')
                        finalPrices.insert(x, 'Not available!')


        return names, urls, originalPrices, finalPrices, images
    # ------------------------------------------------------------------------ #

    # ------------------------ Specific Game --------------------------------- #
    async def getSpecificGame(
        self, 
        gameName: str, 
        language: str,
        currency: str = "br"
    ) -> tuple[str, str, str, str, str, str, str]:
        """Função responsável por retornar as informações e um jogo específico.

        Parameters
        -----------
        gameName: :class:`str`
            Nome do jogo que se deseja obter informações.
        language: :class:`str`
            Linguagem que se deseja visualizar a página do jogo. 
        currency: :class:`str`
            Moeda que se deseja ver o preço.

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
        
        searchUrl = f"{URL_GAME}cc={currency}&l={language}&term={gameName}"
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
                thread5 = executor.submit(
                    self.getGameDescription, 
                    self.reqUrl(thread0.result() + f"&l={language}")
                )

            url          = thread0.result()
            image        = thread1.result()
            name         = thread2.result()
            orginalPrice = thread3.result()
            finalPrice   = thread4.result()
            description  = thread5.result()
        except:
            url = image = name = orginalPrice = finalPrice = description = None

        return name, url, image, orginalPrice, finalPrice, searchUrl.replace(" ", "%20"), description
    # ------------------------------------------------------------------------ #

    # ---------------------- Recommendation By Genre ------------------------- #
    async def getGameRecommendationByGenre(
        self, 
        genre: str,
        currency: str,
        language: str
    ) -> tuple[str, str, str, str, str, str]:
        """Função responsável por recomendar um jogo com base em gênero 
        especificado.

        Parameters
        -----------
        genre: :class:`str`
            Gênero do jogo.
        currency: :class:`str`
            Moeda que se deseja ver o preço.
        language: :class:`str`
            Linguagem que se deseja visualizar a página do jogo. 

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

        genre         = genreFormatting(genre)
        pos           = randint(0, len(TabContent) - 1)
        tabContent    = TabContent(pos).name
        tabContentRow = TabContentRow(pos).name
        url           = f"{URL_GENRE}{genre}/?l={language}&cc={currency}#p=0&tab={tabContent}"

        try:
            (
                gamesNames, 
                gamesUrls, 
                gamesOriginalPrices, 
                gamesFinalPrices, 
                gamesImages
            ) = await self.getTabContent(
                    url      = url, 
                    divId    = tabContentRow,
                    language = language
                )
            
            index             = randint(0, len(gamesNames) - 1)
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
    async def getGameRecommendationByPriceRange(
        self, code: str, 
        maxPrice: str,
        currency: str,
        language:str
    ) -> tuple[str, str, str, str, str]:
        """Função que retorna um jogo com base numa faixa de preço especificada.

        Parameters
        -----------
        code :class:`str`
            Código do preço.
        maxPrice: :class:`str`
            Faixa de preço.
        currency: :class:`str`
            Moeda que se deseja ver o preço.
        language: :class:`str`
            Linguagem que se deseja visualizar a página do jogo. 

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
        
        if(code == "rZ04j"): # Preço maior que R$ 120,00
            url      = f"{URL_PRICE_RANGE}l={language}&cc={currency}"
            maxPrice = "0"
        elif(code == "19Jfc"):  # Preço menor que R$ 10,00
            url      = f"{URL_PRICE_RANGE}l={language}&maxprice=10&cc={currency}"
            maxPrice = "10"
        else:
            url = f"{URL_PRICE_RANGE}l={language}&maxprice={maxPrice}&cc={currency}"

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

        index = verifyPriceRange(maxPrice=float(maxPrice), gameFinalPrices=gameFinalPrices)

        gameName        = gameNames[index]
        gameImage       = gameImages[index]
        gameUrl         = gameUrls[index]
        gameOrinalPrice = gameOrinalPrices[index]
        gameFinalPrice  = gameFinalPrices[index]

        return gameName, gameImage, gameUrl, gameOrinalPrice, gameFinalPrice
    # ------------------------------------------------------------------------ #

    # ------------------------- Game By Link --------------------------------- #
    async def getGameByLink(
        self, 
        url: str,
        currency: str,
        language:str
    ) -> tuple[str, str, str, str, str]:
        """Função responsável por retornar um jogo com base no link enviado.

        Parameters
        -----------
        url: :class:`str`
            URL do jogo enviada.
        currency: :class:`str`
            Moeda que se deseja ver o preço.
        language: :class:`str`
            Linguagem que se deseja visualizar a página do jogo. 

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
        
        soup = self.reqUrl(url + f"?cc={currency}&l={language}")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            thread0 = executor.submit(getGameByLinkName, soup)
            thread1 = executor.submit(getGameByLinkImage, soup)
            thread2 = executor.submit(getGameByLinkOriginalPrice, soup)
            thread3 = executor.submit(getGameByLinkFinalPrice, soup)
            thread4 = executor.submit(
                self.getGameDescription, 
                soup
            )

        name          = thread0.result()
        image         = thread1.result()
        description   = thread4.result()

        # Verificação de incoerências nos preços.
        (
            orginalPrice, 
            finalPrice
        ) = handlePriceIssues(
                originalPrices=[thread2.result()], 
                finalPrices=[thread3.result()]
            )

        return name, image, orginalPrice[0], finalPrice[0], description
    # ------------------------------------------------------------------------ #

    # ------------------------- Game Reviews --------------------------------- #
    async def getGameReview(self, url: str) -> tuple[list, list]:
        """Função responsável por retornar um resumo das análises de um jogo 
        com base na url.

        Parameters
        -----------
        url: :class:`str`
            Url do jogo.

        Returns
        -----------
        sumary: :class:`str`
            Resumo das análises do jogo.
        totalAmount: :class:`str`
            Quantidade total de análises do jogo.
        """

        soup = self.reqUrl(url)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            thread0 = executor.submit(getReviewSumary, soup)
            thread1 = executor.submit(getReviewTotalAmount, soup)

        sumary      = thread0.result()
        totalAmount = thread1.result()

        return sumary, totalAmount
    # ------------------------------------------------------------------------ #