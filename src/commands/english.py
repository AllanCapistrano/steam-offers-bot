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

class CommandsEnglish(Commands, commands.Cog):
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"\nO {self.client.user.name} está escutando os comandos em Inglês.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
        if(isinstance(error, commands.CommandNotFound)):
            await ctx.send(self.message.commandAlert(language="en")[2])
        if(isinstance(error, commands.DisabledCommand)):
            if(ctx.cog.qualified_name == "CommandsEnglish"):
                await ctx.send(self.message.commandAlert(language="en")[5])

    @commands.group(name="help", aliases=["commands"])
    async def help(self, ctx: Context):
        if(ctx.subcommand_passed is None):
            embedHelp = EmbedHelp(
                client    = self.client,
                prefix    = self.prefix,
                color     = self.color,
                message   = self.message
            )

            await ctx.send(embed=embedHelp.embedHelpEnglish())
        elif(
            ctx.subcommand_passed != "genre" and 
            ctx.subcommand_passed != "gametab"
        ):
            raise commands.CommandNotFound()

    @help.command(name="genre")
    async def helpGenre(self, ctx: Context):
        embedHelpGenre = EmbedHelpGenre(
            prefix    = self.prefix,
            color     = self.color,
            message   = self.message,
            imgGenres = self.imgGenre
        )

        await ctx.send(embed=embedHelpGenre.embedHelpGenreEnglish())
    
    @help.command(name="gametab")
    async def helpGameTab(self, ctx: Context):
        embedHelpGameTab = EmbedHelpGameTab(
            client  = self.client,
            prefix  = self.prefix,
            color   = self.color,
            message = self.message
        )

        await ctx.send(embed=embedHelpGameTab.embedHelpGameTabEnglish())

    @commands.command(name="invite")
    async def invite(self, ctx: Context):
        embedInvite = EmbedInvite(
            client    = self.client,
            color     = self.color,
            message   = self.message,
            urlInvite = self.urlInvite
        )

        await ctx.send(embed=embedInvite.embedInviteEnglish())

    @commands.command(name="spotlight", aliases=["sl"])
    async def spotlightOffers(self, ctx: Context):
        # Mensagem de busca, com efeito de carregamento.
        messageContent = self.message.searchMessage(language="en")[0]
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
            await searchMessage.edit(content=self.message.noOffers(language="en")[0])
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
                        embed   = embedSpotlightGames.embedSpotlightGameEnglish()
                    )
                else:
                    await ctx.send(
                        embed=embedSpotlightGames.embedSpotlightGameEnglish()
                    )

                x -= 1

    @commands.command(name="dailydeal ", aliases=["dd"])
    async def dailyGamesOffers(self, ctx: Context):
        # Mensagem de busca, com efeito de carregamento.
        messageContent = self.message.searchMessage(language="en")[0]
        searchMessage  = await ctx.send(messageContent)
        
        sleep(0.5)
        await searchMessage.edit(content=messageContent+" **.**")
        
        sleep(0.5)
        await searchMessage.edit(content=messageContent+" **. .**")

        (
            gamesUrls, 
            gamesImages,
            gamesOriginalPrices,
            gamesFinalPrices
        ) = await self.crawler.getDailyGamesOffers()
        x = len(gamesUrls)

        if(
            len(gamesUrls)           == 0 or
            len(gamesImages)         == 0 or
            len(gamesOriginalPrices) == 0 or
            len(gamesFinalPrices)    == 0
        ):
            await searchMessage.edit(content=self.message.noOffers(language="en")[1])
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
                        embed   = embedDailyGames.embedDailyGameEnglish()
                    )
                else:
                    await ctx.send(
                        embed=embedDailyGames.embedDailyGameEnglish()
                    )
                
                x -= 1

    @commands.command(name="info")
    async def botInfo(self, ctx: Context):
        embedBotInfo = EmbedBotInfo(
            client  = self.client,
            color   = self.color,
            message = self.message,
            ownerId = self.ownerId
        )

        await ctx.send(embed=embedBotInfo.embedBotInfoEnglish())

    @commands.group(name="gametab")
    async def gameTab(self, ctx: Context):
        # Caso o subcomando não seja passado ou seja inválido.
        if(ctx.invoked_subcommand is None):
            await ctx.send(self.message.commandAlert(language="en", prefix=self.prefix)[3])
        
    @gameTab.command(
        name="new-tranding", 
        aliases=[
            "newtranding",
            "nt"
        ]
    )
    async def newAndTrending(self, ctx: Context):
        (
            gamesNames, 
            gamesUrls, 
            gamesOriginalPrices, 
            gamesFinalPrices, 
            gamesImages
        ) = await self.crawler.getTabContent(url=self.url+"NewReleases", divId="NewReleasesRows")

        await self.sendGameTabToUser(
            ctx=ctx,
            gamesNames=gamesNames,
            gamesUrls=gamesUrls,
            gamesOriginalPrices=gamesOriginalPrices,
            gamesFinalPrices=gamesFinalPrices,
            language="en"
        )
    
    @gameTab.command(
        name="top-sellers", 
        aliases=[
            "topsellers",
            "ts"
        ]
    )
    async def topSellers(self, ctx: Context):
        (
            gamesNames, 
            gamesUrls, 
            gamesOriginalPrices, 
            gamesFinalPrices, 
            gamesImages
        ) = await self.crawler.getTabContent(url=self.url+"TopSellers", divId="TopSellersRows")

        await self.sendGameTabToUser(
            ctx=ctx,
            gamesNames=gamesNames,
            gamesUrls=gamesUrls,
            gamesOriginalPrices=gamesOriginalPrices,
            gamesFinalPrices=gamesFinalPrices,
            language="en"
        )

    @gameTab.command(
        name="being-played", 
        aliases=[
            "beingplayed",
            "bp"
        ]
    )
    async def beingPlayed(self, ctx: Context):
        (
            gamesNames, 
            gamesUrls, 
            gamesOriginalPrices, 
            gamesFinalPrices, 
            gamesImages
        ) = await self.crawler.getTabContent(url=self.url+"ConcurrentUsers", divId="ConcurrentUsersRows")

        await self.sendGameTabToUser(
            ctx=ctx,
            gamesNames=gamesNames,
            gamesUrls=gamesUrls,
            gamesOriginalPrices=gamesOriginalPrices,
            gamesFinalPrices=gamesFinalPrices,
            language="en"
        )

    @gameTab.command(
        name="pre-purchase", 
        aliases=[
            "prepurchase",
            "pp"
        ]
    )
    async def prePurchase(self, ctx: Context):
        (
            gamesNames, 
            gamesUrls, 
            gamesOriginalPrices, 
            gamesFinalPrices, 
            gamesImages
        ) = await self.crawler.getTabContent(url=self.url+"ComingSoon", divId="ComingSoonRows")

        await self.sendGameTabToUser(
            ctx=ctx,
            gamesNames=gamesNames,
            gamesUrls=gamesUrls,
            gamesOriginalPrices=gamesOriginalPrices,
            gamesFinalPrices=gamesFinalPrices,
            language="en"
        )
    
    @commands.command(name="game")
    async def specificGame(self, ctx: Context, *, args: str):
        gameToSearch = args

        # Mensagem de busca de jogo, com efeito de carregamento.
        messageContent    = self.message.searchMessage(language="en")[1]
        searchGameMessage = await ctx.send(messageContent + " __"+ gameToSearch + "__ .**")
        
        sleep(0.5)
        await searchGameMessage.edit(content=messageContent + " __" + gameToSearch + "__ . .**")
        
        sleep(0.5)
        await searchGameMessage.edit(content=messageContent + " __"+ gameToSearch + "__ . . .**")

        embedSpecificGame = await specificGameEmbed(
            crawler      = self.crawler, 
            embedColor   = self.color, 
            gameToSearch = gameToSearch,
            language     = "en"
        )

        if(embedSpecificGame != None):
            await searchGameMessage.edit(content="", embed=embedSpecificGame)
            await searchGameMessage.add_reaction(self.reactions[0])
        else:
            await searchGameMessage.edit(content=self.message.noOffers(language="en")[2])

    @specificGame.error
    async def specificGameError(self, ctx: Context, error: CommandError):
        if(isinstance(error, commands.MissingRequiredArgument)):
            if(error.param.name == "args"):
                await ctx.send(self.message.commandAlert(language="en", prefix=self.prefix)[0])

    @commands.command(name="genre")
    async def gameGenre(self, ctx: Context, *, args: str):
        gameGenreToSearch = args

        # Mensagem de busca, com efeito de carregamento.
        messageContent      = self.message.searchMessage(language="en")[2]
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
        ) = await self.crawler.getGameRecommendationByGenre(gameGenreToSearch)

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
                embed   = embedGenre.embedGenreEnglish()
            )
            await searchGenreMessage.add_reaction(self.reactions[0])
        else:
            await searchGenreMessage.edit(content=self.message.noOffers(language="en", prefix=self.prefix)[3])

    @gameGenre.error
    async def gameGenreError(self, ctx: Context, error: CommandError):
        if(isinstance(error, commands.MissingRequiredArgument)):
            if(error.param.name == "args"):
                await ctx.send(self.message.commandAlert(prefix=self.prefix)[1])

    @commands.command(name="maxprice")
    async def maxPrice(self, ctx: Context, *, args: str):
        if(not args.isnumeric()):
            raise commands.ArgumentParsingError()
        
        maxPrice = args

        # Mensagem de busca de jogo, com efeito de carregamento.
        messageContent    = self.message.searchMessage(language="en")[3]
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
                maxPrice = float(maxPrice)
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
            embed   = embedGameRecommendationByPrice.embedSpecificGameEnglish()
        )
        await searchGameMessage.add_reaction(self.reactions[0])
        
    @maxPrice.error
    async def maxPriceError(self, ctx: Context, error: CommandError):
        if(isinstance(error, commands.MissingRequiredArgument)):
            if(error.param.name == "args"):
                await ctx.send(self.message.recommendationByPrice(language="en")[3])
        if(isinstance(error, commands.ArgumentParsingError)):
            await ctx.send(self.message.recommendationByPrice(language="en")[0])
    
    @commands.command(name="review", aliases=["reviews"])
    async def review(self, ctx: Context, *, args: str):
        gameToSearch = args

        # Mensagem de busca, com efeito de carregamento.
        messageContent = self.message.searchMessage(language="en")[0]
        searchMessage  = await ctx.send(messageContent)
        
        sleep(0.5)
        await searchMessage.edit(content = messageContent+" **.**")
        
        sleep(0.5)
        await searchMessage.edit(content = messageContent+" **. .**")

        embedGameReview = await gameReviewEmbed(
            crawler      = self.crawler,
            embedColor   = self.color,
            gameToSearch = gameToSearch,
            language     = "en"
        )

        if(embedGameReview != None):
            await searchMessage.edit(content="", embed=embedGameReview)
            await searchMessage.add_reaction(self.reactions[1])
        else:
            await searchMessage.edit(content=self.message.noOffers(language="en")[2])

    @review.error
    async def reviewError(self, ctx: Context, error: CommandError):
        if(isinstance(error, commands.MissingRequiredArgument)):
            if(error.param.name == "args"):
                await ctx.send(self.message.commandAlert(prefix=self.prefix)[4])