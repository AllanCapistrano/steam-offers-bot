from time import sleep

from discord.ext import commands
from discord.ext.commands import Context, CommandError

from commands.commands import Commands
from services.SpecificGame.specificGameEmbed import specificGameEmbed
from services.GameReview.gameReviewEmbed import gameReviewEmbed
from embeds.embedHelp import EmbedHelp
from embeds.embedHelpGenre import EmbedHelpGenre
from embeds.embedHelpGameTab import EmbedHelpGameTab
from embeds.embedInvite import EmbedInvite
from embeds.embedBotInfo import EmbedBotInfo
from embeds.embedGameRecommendationByPrice import EmbedGameRecommendationByPrice
from embeds.embedGenre import EmbedGenre
from embeds.embedSpotlightGame import EmbedSpotlightGame
from embeds.embedDailyGame import EmbedDailyGame
from embeds.embedCurrency import EmbedCurrency

# ------------------------------ Constants ----------------------------------- #
LANGUAGE = "brazilian"
# ---------------------------------------------------------------------------- #
class CommandsBrazilianPortuguese(Commands, commands.Cog):
    @commands.Cog.listener()
    async def on_ready(self):
        print(
            f"\nO {self.client.user.name} está escutando os comandos em " + \
            "Português Brasileiro."
        )

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
        if(isinstance(error, commands.CommandNotFound)):
            await ctx.send(self.message.commandAlert()[2])
        if(isinstance(error, commands.DisabledCommand)):
            if(ctx.cog.qualified_name == "CommandsBrazilianPortuguese"):
                await ctx.send(self.message.commandAlert()[5])
        if(isinstance(error, commands.BadArgument)):
            if(ctx.cog.qualified_name == "CommandsBrazilianPortuguese"):
                await ctx.send(self.message.commandAlert()[2])

    @commands.group(name="ajuda", aliases=["comandos"])
    async def help(self, ctx: Context):
        if(ctx.subcommand_passed is None):
            embedHelp = EmbedHelp(
                client    = self.client,
                prefix    = self.prefix,
                color     = self.color,
                message   = self.message
            )

            await ctx.send(embed=embedHelp.embedHelpPortuguese())
        elif(
            ctx.subcommand_passed != "gênero" and 
            ctx.subcommand_passed != "genero" and 
            ctx.subcommand_passed != "categoria" and
            ctx.subcommand_passed != "moedas" 
        ):
            raise commands.BadArgument()

    @help.command(name="gênero", aliases=["genero"])
    async def helpGenre(self, ctx: Context):
        embedHelpGenre = EmbedHelpGenre(
            prefix    = self.prefix,
            color     = self.color,
            message   = self.message,
            imgGenres = self.imgGenre
        )

        await ctx.send(embed=embedHelpGenre.embedHelpGenrePortuguese())
    
    @help.command(name="categoria")
    async def helpGameTab(self, ctx: Context):
        embedHelpGameTab = EmbedHelpGameTab(
            client  = self.client,
            prefix  = self.prefix,
            color   = self.color,
            message = self.message
        )

        await ctx.send(embed=embedHelpGameTab.embedHelpGameTabPortuguese())

    @help.command(name="moedas")
    async def helpCurrencies(self, ctx: Context):
        embedHelpCurrency = EmbedCurrency(
            color   = self.color,
            message = self.message
        )

        messageSent = await ctx.send(embed=embedHelpCurrency.embedCurrencyPortuguese(end=24))

        await messageSent.add_reaction(self.reactions[2])

    @commands.command(name="convite")
    async def invite(self, ctx: Context):
        embedInvite = EmbedInvite(
            client    = self.client,
            color     = self.color,
            message   = self.message,
            urlInvite = self.urlInvite
        )

        await ctx.send(embed=embedInvite.embedInvitePortuguese())

    @commands.command(name="destaque", aliases=["dt"])
    async def spotlightOffers(self, ctx: Context):
        # Mensagem de busca, com efeito de carregamento.
        messageContent = self.message.searchMessage()[0]
        searchMessage  = await ctx.send(messageContent)
        
        sleep(0.5)
        await searchMessage.edit(content=messageContent+" **.**")
        
        sleep(0.5)
        await searchMessage.edit(content=messageContent+" **. .**")

        (
            gamesUrls, 
            gamesImages, 
            gamesContents
        ) = await self.crawler.getSpotlightOffers()
        x = len(gamesUrls)

        if(
            len(gamesUrls)     == 0 or
            len(gamesImages)   == 0 or
            len(gamesContents) == 0
        ):
            await searchMessage.edit(content=self.message.noOffers()[0])
        else:
            firstIteration = True

            while(x > 0):
                embedSpotlightGames = EmbedSpotlightGame(
                    color       = self.color,
                    gameImg     = gamesImages[x - 1],
                    gameUrl     = gamesUrls[x - 1]["value"],
                    gameContent = gamesContents[x - 1]["value"],
                    message     = self.message
                )

                if(firstIteration):
                    firstIteration = False
                    
                    await searchMessage.edit(
                        content = "", 
                        embed   = embedSpotlightGames.embedSpotlightGamePortuguese()
                    )
                else:
                    await ctx.send(
                        embed=embedSpotlightGames.embedSpotlightGamePortuguese()
                    )

                x -= 1

    @commands.command(name="promoção", aliases=["promocao", "pr"])
    async def dailyGamesOffers(self, ctx: Context, *args: str):
        # Mensagem de busca, com efeito de carregamento.
        messageContent = self.message.searchMessage()[0]
        searchMessage  = await ctx.send(messageContent)
        currency       = self.currency.defineCurrency(args=args)
        
        sleep(0.5)
        await searchMessage.edit(content=messageContent+" **.**")
        
        sleep(0.5)
        await searchMessage.edit(content=messageContent+" **. .**")

        (
            gamesUrls, 
            gamesImages,
            gamesOriginalPrices,
            gamesFinalPrices
        ) = await self.crawler.getDailyGamesOffers(
            currency = currency,
            language = LANGUAGE
        )
        x = len(gamesUrls)

        if(
            len(gamesUrls)           == 0 or
            len(gamesImages)         == 0 or
            len(gamesOriginalPrices) == 0 or
            len(gamesFinalPrices)    == 0
        ):
            await searchMessage.edit(content=self.message.noOffers()[1])
        else:
            firstIteration = True

            while(x > 0):
                embedDailyGames = EmbedDailyGame(
                    color             = self.color,
                    gameImg           = gamesImages[x - 1],
                    gameUrl           = gamesUrls[x - 1],
                    gameOriginalPrice = gamesOriginalPrices[x - 1],
                    gameFinalPrice    = gamesFinalPrices[x - 1],
                    message           = self.message
                )

                if(firstIteration):
                    firstIteration = False

                    await searchMessage.edit(
                        content = "", 
                        embed   = embedDailyGames.embedDailyGamePortuguese()
                    )
                else:
                    await ctx.send(
                        embed=embedDailyGames.embedDailyGamePortuguese()
                    )
                
                x -= 1

    @commands.command(name="botinfo")
    async def botInfo(self, ctx: Context):
        embedBotInfo = EmbedBotInfo(
            client  = self.client,
            color   = self.color,
            message = self.message,
            ownerId = self.ownerId
        )

        await ctx.send(embed=embedBotInfo.embedBotInfoPortuguese())

    @commands.group(name="categoria")
    async def gameTab(self, ctx: Context):
        # Caso o subcomando não seja passado ou seja inválido.
        if(ctx.invoked_subcommand is None):
            await ctx.send(self.message.commandAlert(prefix=self.prefix)[3])
        
    @gameTab.command(
        name="novidades-populares", 
        aliases=[
            "novidadespopulares",
            "np"
        ]
    )
    async def newAndTrending(self, ctx: Context, *args: str):
        currency = self.currency.defineCurrency(args=args)

        (
            gamesNames, 
            gamesUrls, 
            gamesOriginalPrices, 
            gamesFinalPrices, 
            gamesImages
        ) = await self.crawler.getTabContent(
                currency = currency, 
                language = LANGUAGE,
                category = "NewReleases",
                divId    = "NewReleasesRows"
            )

        await self.sendGameTabToUser(
            ctx                 = ctx,
            gamesNames          = gamesNames,
            gamesUrls           = gamesUrls,
            gamesOriginalPrices = gamesOriginalPrices,
            gamesFinalPrices    = gamesFinalPrices
        )
    
    @gameTab.command(
        name="mais-vendidos", 
        aliases=[
            "maisvendidos",
            "mv"
        ]
    )
    async def topSellers(self, ctx: Context, *args: str):
        currency = self.currency.defineCurrency(args=args)

        (
            gamesNames, 
            gamesUrls, 
            gamesOriginalPrices, 
            gamesFinalPrices, 
            gamesImages
        ) = await self.crawler.getTabContent(
                currency = currency, 
                language = LANGUAGE,
                category = "TopSellers",
                divId    = "TopSellersRows"
            )

        await self.sendGameTabToUser(
            ctx                 = ctx,
            gamesNames          = gamesNames,
            gamesUrls           = gamesUrls,
            gamesOriginalPrices = gamesOriginalPrices,
            gamesFinalPrices    = gamesFinalPrices
        )

    @gameTab.command(
        name="jogos-populares", 
        aliases=[
            "jogospopulares",
            "jp"
        ]
    )
    async def beingPlayed(self, ctx: Context, *args: str):
        currency = self.currency.defineCurrency(args=args)

        (
            gamesNames, 
            gamesUrls, 
            gamesOriginalPrices, 
            gamesFinalPrices, 
            gamesImages
        ) = await self.crawler.getTabContent(
                currency = currency,
                language = LANGUAGE,
                category = "ConcurrentUsers",
                divId    = "ConcurrentUsersRows"
            )

        await self.sendGameTabToUser(
            ctx                 = ctx,
            gamesNames          = gamesNames,
            gamesUrls           = gamesUrls,
            gamesOriginalPrices = gamesOriginalPrices,
            gamesFinalPrices    = gamesFinalPrices
        )

    @gameTab.command(
        name="pré-venda", 
        aliases=[
            "prévenda",
            "pre-venda",
            "prevenda",
            "pv"
        ]
    )
    async def prePurchase(self, ctx: Context, *args: str):
        currency = self.currency.defineCurrency(args=args)

        (
            gamesNames, 
            gamesUrls, 
            gamesOriginalPrices, 
            gamesFinalPrices, 
            gamesImages
        ) = await self.crawler.getTabContent(
                currency = currency,
                language = LANGUAGE,
                category = "ComingSoon",
                divId    ="ComingSoonRows"
            )

        await self.sendGameTabToUser(
            ctx                 = ctx,
            gamesNames          = gamesNames,
            gamesUrls           = gamesUrls,
            gamesOriginalPrices = gamesOriginalPrices,
            gamesFinalPrices    = gamesFinalPrices
        )
    
    @commands.command(name="jogo")
    async def specificGame(self, ctx: Context, *, args: str):
        gameToSearch = args.split(" | ")[0]
        currency     = self.currency.defineCurrency(args=args)

        # Mensagem de busca de jogo, com efeito de carregamento.
        messageContent    = self.message.searchMessage()[1]
        searchGameMessage = await ctx.send(messageContent + " __"+ gameToSearch + "__ .**")
        
        sleep(0.5)
        await searchGameMessage.edit(content=messageContent + " __" + gameToSearch + "__ . .**")
        
        sleep(0.5)
        await searchGameMessage.edit(content=messageContent + " __"+ gameToSearch + "__ . . .**")

        embedSpecificGame = await specificGameEmbed(
            crawler      = self.crawler, 
            embedColor   = self.color, 
            gameToSearch = gameToSearch,
            currency     = currency,
            language     = LANGUAGE
        )

        if(embedSpecificGame != None):
            await searchGameMessage.edit(content="", embed=embedSpecificGame)
            await searchGameMessage.add_reaction(self.reactions[0])
        else:
            await searchGameMessage.edit(content=self.message.noOffers()[2])

    @specificGame.error
    async def specificGameError(self, ctx: Context, error: CommandError):
        if(isinstance(error, commands.MissingRequiredArgument)):
            if(error.param.name == "args"):
                await ctx.send(self.message.commandAlert(prefix=self.prefix)[0])

    @commands.command(name="gênero", aliases=["genero"])
    async def gameGenre(self, ctx: Context, *, args: str):
        gameGenreToSearch = args.split(" | ")[0]
        currency          = self.currency.defineCurrency(args=args)

        # Mensagem de busca, com efeito de carregamento.
        messageContent      = self.message.searchMessage()[2]
        searchGenreMessage  = await ctx.send(messageContent + " __"+ gameGenreToSearch +"__ .**")
        
        sleep(0.5)
        await searchGenreMessage.edit(content=messageContent + " __" + gameGenreToSearch + "__ . .**")
        
        sleep(0.5)
        await searchGenreMessage.edit(content=messageContent + " __" + gameGenreToSearch + "__ . . .**")

        (
            gameName, 
            gameURL, 
            gameOriginalPrice, 
            gameFinalPrice, 
            gameIMG
        ) = await self.crawler.getGameRecommendationByGenre(
                genre    = gameGenreToSearch,
                currency = currency,
                language = LANGUAGE
            )

        if(
            gameName          != None and 
            gameURL           != None and 
            gameOriginalPrice != None and
            gameFinalPrice    != None and
            gameIMG           != None
        ):
            embedGenre = EmbedGenre(
                color             = self.color,
                gameGenreToSearch = gameGenreToSearch,
                gameName          = gameName,
                gameImg           = gameIMG,
                gameUrl           = gameURL,
                gameOriginalPrice = gameOriginalPrice,
                gameFinalPrice    = gameFinalPrice,
                message           = self.message
            )

            await searchGenreMessage.edit(
                content = "", 
                embed   = embedGenre.embedGenrePortuguese()
            )
            await searchGenreMessage.add_reaction(self.reactions[0])
        else:
            await searchGenreMessage.edit(content=self.message.noOffers(prefix=self.prefix)[3])

    @gameGenre.error
    async def gameGenreError(self, ctx: Context, error: CommandError):
        if(isinstance(error, commands.MissingRequiredArgument)):
            if(error.param.name == "args"):
                await ctx.send(self.message.commandAlert(prefix=self.prefix)[1])

    @commands.command(
        name="preçomáximo", 
        aliases=[
            "precomaximo", 
            "preçomaximo", 
            "precomáximo"
        ]
    )
    async def maxPrice(self, ctx: Context, *, args: str):
        maxPrice = args.split(" | ")[0]

        if(not maxPrice.isnumeric()):
            raise commands.ArgumentParsingError()
        
        currency = self.currency.defineCurrency(args=args)

        # Mensagem de busca de jogo, com efeito de carregamento.
        messageContent    = self.message.searchMessage()[3]
        searchGameMessage = await ctx.send(messageContent + " "+ maxPrice + "__ .**")
        
        sleep(0.5)
        await searchGameMessage.edit(content=messageContent + " " + maxPrice + "__ . .**")
        
        sleep(0.5)
        await searchGameMessage.edit(content=messageContent + " "+ maxPrice + "__ . . .**")

        if(float(maxPrice) > 120):
            maxPriceCode = "rZ04j" # Preço maior que $120,00
        elif(float(maxPrice) < 10):
            maxPriceCode = "19Jfc" # Preço menor que $10,00
        else:
            maxPriceCode = None
        
        (
            gameName,
            gameIMG, 
            gameURL, 
            gameOriginalPrice,
            gameFinalPrice
        ) = await self.crawler.getGameRecommendationByPriceRange(
                code     = maxPriceCode, 
                maxPrice = float(maxPrice),
                currency = currency,
                language = LANGUAGE
            )

        embedGameRecommendationByPrice = EmbedGameRecommendationByPrice(
            color             = self.color,
            gameName          = gameName,
            gameImg           = gameIMG,
            gameUrl           = gameURL,
            gameOriginalPrice = gameOriginalPrice,
            gameFinalPrice    = gameFinalPrice,
            maxPriceCode      = maxPriceCode,
            message           = self.message
        )
        
        await searchGameMessage.edit(
            content = "", 
            embed   = embedGameRecommendationByPrice.embedSpecificGamePortuguese()
        )
        await searchGameMessage.add_reaction(self.reactions[0])
        
    @maxPrice.error
    async def maxPriceError(self, ctx: Context, error: CommandError):
        if(isinstance(error, commands.MissingRequiredArgument)):
            if(error.param.name == "args"):
                await ctx.send(self.message.recommendationByPrice()[3])
        if(isinstance(error, commands.ArgumentParsingError)):
            await ctx.send(self.message.recommendationByPrice()[0])
    
    @commands.command(
        name="análise", 
        aliases=[
            "analise", 
            "análises", 
            "analises"
        ]
    )
    async def review(self, ctx: Context, *, args: str):
        gameToSearch = args

        # Mensagem de busca, com efeito de carregamento.
        messageContent = self.message.searchMessage()[0]
        searchMessage  = await ctx.send(messageContent)
        
        sleep(0.5)
        await searchMessage.edit(content = messageContent+" **.**")
        
        sleep(0.5)
        await searchMessage.edit(content = messageContent+" **. .**")

        embedGameReview = await gameReviewEmbed(
            crawler      = self.crawler,
            embedColor   = self.color,
            gameToSearch = gameToSearch
        )

        if(embedGameReview != None):
            await searchMessage.edit(content="", embed=embedGameReview)
            await searchMessage.add_reaction(self.reactions[1])
        else:
            await searchMessage.edit(content=self.message.noOffers()[2])

    @review.error
    async def reviewError(self, ctx: Context, error: CommandError):
        if(isinstance(error, commands.MissingRequiredArgument)):
            if(error.param.name == "args"):
                await ctx.send(self.message.commandAlert(prefix=self.prefix)[4])

    @commands.command(name="toggle", aliases=["ativar"])
    @commands.is_owner()
    async def toggleCommand(self, ctx: Context, *, args: str):
        command = self.client.get_command(args)

        # Caso o comando não seja encontrado.
        if(command == None):
            await ctx.send(self.message.commandAlert()[6])
        elif(ctx.command == command): # Caso tente desabilitar este comando.
            await ctx.send(self.message.commandAlert()[7])
        else:
            command.enabled = not command.enabled
            
            status = "habilitado" if command.enabled == True else "desabilitado"
            
            await ctx.send(
                self.message.commandAlert(
                    prefix  = self.prefix, 
                    command = command, 
                    status  = status
                )[8]
            )