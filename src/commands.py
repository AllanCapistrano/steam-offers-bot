from time import sleep
from typing import Literal

from discord import Embed
from discord.ext import commands
from discord.ext.commands import Bot, Context, CommandError

from services.crawler import Crawler
from services.messages import Message
from services.SpecificGame.specificGameEmbed import specificGameEmbed
from services.GameReview.gameReviewEmbed import gameReviewEmbed
from embeds.embedHelp import EmbedHelp
from embeds.embedHelpGenre import EmbedHelpGenre
from embeds.embedHelpGameTab import EmbedHelpGameTab
from embeds.embedInvite import EmbedInvite
from embeds.embedBotInfo import EmbedBotInfo

# ------------------------------ Constants ----------------------------------- #
IMG_GENRES = ["https://i.imgur.com/q0NfeWX.png", "https://i.imgur.com/XkSXCZy.png"]
URL        = "https://store.steampowered.com/specials?cc=br#p=0&tab="
# ---------------------------------------------------------------------------- #

class Commands(commands.Cog):
    def __init__(
        self, 
        client: Bot, 
        prefix: str, 
        color: Literal, 
        urlInvite: str,
        reactions: list
    ) -> None:
        """ Método construtor.

        Parameters
        -----------
        client: :class:`Bot`
        prefix: :class:`str`
        color: :class:`Literal`
        urlInvite: :class:`str`
        reactions: :class:`list`
        """
    
        self.client    = client
        self.prefix    = prefix
        self.color     = color
        self.urlInvite = urlInvite
        self.ownerId   = 259443927441080330
        self.reactions = reactions
        self.message   = Message()
        self.crawler   = Crawler()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"\nO {self.client.user.name} está escutando os comandos.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
        if(isinstance(error, commands.CommandNotFound)):
            await ctx.send(self.message.commandAlert()[2])
        if(isinstance(error, commands.DisabledCommand)):
            await ctx.send(self.message.commandAlert()[5])

    @commands.group(name="help", aliases=["ajuda", "comandos"])
    async def help(self, ctx: Context):
        if(ctx.subcommand_passed is None):
            embedHelp = EmbedHelp(
                client    = self.client,
                prefix    = self.prefix,
                color     = self.color,
                message   = self.message
            )

            await ctx.send(embed=embedHelp.embedHelpPortuguese())
        elif(ctx.subcommand_passed != "genre" and ctx.subcommand_passed != "gametab"):
            raise commands.CommandNotFound()

    @help.command(name="genre")
    async def helpGenre(self, ctx: Context):
        embedHelpGenre = EmbedHelpGenre(
            prefix    = self.prefix,
            color     = self.color,
            message   = self.message,
            imgGenres = IMG_GENRES
        )

        await ctx.send(embed=embedHelpGenre.embedHelpGenrePortuguese())
    
    @help.command(name="gametab")
    async def helpGameTab(self, ctx: Context):
        embedHelpGameTab = EmbedHelpGameTab(
            client  = self.client,
            prefix  = self.prefix,
            color   = self.color,
            message = self.message
        )

        await ctx.send(embed=embedHelpGameTab.embedHelpGameTabPortuguese())

    @commands.command(name="invite", aliases=["convite"])
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

        if(x == 0):
            await searchMessage.edit(content=self.message.noOffers()[0])
        else:
            firstIteration = True

            while(x > 0):
                embedSpotlightGames = Embed(
                    title = self.message.title()[1],
                    color = self.color
                )
                embedSpotlightGames.set_image(url=gamesImages[x - 1])
                embedSpotlightGames.add_field(
                    name   = "**Link:**", 
                    value  = "**[Clique Aqui]({})**".format(gamesUrls[x - 1]["value"]), 
                    inline = False
                )
                embedSpotlightGames.add_field(
                    name   = "**Descrição:**", 
                    value  = "**{}**".format(gamesContents[x - 1]["value"]), 
                    inline = False
                )

                if(firstIteration):
                    firstIteration = False
                    
                    await searchMessage.edit(content="", embed=embedSpotlightGames)
                else:
                    await ctx.send(embed=embedSpotlightGames)

                x -= 1

    @commands.command(name="promoção", aliases=["promocao", "pr"])
    async def dailyGamesOffers(self, ctx: Context):
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
            await searchMessage.edit(content=self.message.noOffers()[1])
        else:
            firstIteration = True

            while(x > 0):
                embedDailyGames = Embed(
                    title = self.message.title()[2],
                    color = self.color
                )
                embedDailyGames.set_image(url=gamesImages[x - 1])
                embedDailyGames.add_field(
                    name   = "**Link:**", 
                    value  = f"**[Clique Aqui]({gamesUrls[x - 1]})**", 
                    inline = False
                )

                if(gamesOriginalPrices[x - 1] == gamesFinalPrices[x - 1]):
                    embedDailyGames.add_field(
                        name   = "**Preço:**", 
                        value  = f"**{gamesOriginalPrices[x - 1]}**", 
                        inline = True
                    )
                else:
                    embedDailyGames.add_field(
                        name   = "**Preço Original:**", 
                        value  = f"**{gamesOriginalPrices[x - 1]}**", 
                        inline = True
                    )
                    embedDailyGames.add_field(
                        name   = "**Preço com Desconto:**", 
                        value  = f"**{gamesFinalPrices[x - 1]}**", 
                        inline = True
                    )

                if(firstIteration):
                    firstIteration = False

                    await searchMessage.edit(content="", embed=embedDailyGames)
                else:
                    await ctx.send(embed=embedDailyGames)
                
                x -= 1

    @commands.command(name="botinfo", aliases=["info"])
    async def botInfo(self, ctx: Context):
        # embedBotInfo = Embed(
        #     title = self.message.title()[3],
        #     color = self.color
        # )
        # embedBotInfo.set_thumbnail(url=self.client.user.avatar_url)
        # embedBotInfo.add_field(
        #     name   = "Python", 
        #     value  = self.message.infoValues()[0], 
        #     inline = True
        # )
        # embedBotInfo.add_field(
        #     name   = "discord.py", 
        #     value  = self.message.infoValues()[1], 
        #     inline = True
        # )
        # embedBotInfo.add_field(
        #     name   = "Sobre {}".format(self.client.user.name), 
        #     value  = self.message.infoValues()[2] + 
        #     self.client.get_user(self.ownerId).name + "#" 
        #     + self.client.get_user(self.ownerId).discriminator + "**", 
        #     inline = False
        # )
        # embedBotInfo.set_author(
        #     name     = self.client.get_user(self.ownerId).name + "#" 
        #     + self.client.get_user(self.ownerId).discriminator, 
        #     icon_url = self.client.get_user(self.ownerId).avatar_url
        # )
        # embedBotInfo.set_footer(
        #     text="Criado em 26 de Maio de 2020! | Última atualização em {}."
        #     .format(self.message.infoValues()[3])
        # )

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
            await ctx.send(self.message.commandAlert(self.prefix)[3])
        
    @gameTab.command(
        name="novidades populares", 
        aliases=[
            "novidadespopulares",
            "novidades", 
            "populares", 
            "np"
        ]
    )
    async def newAndTrending(self, ctx: Context):
        (
            gamesNames, 
            gamesUrls, 
            gamesOriginalPrices, 
            gamesFinalPrices, 
            gamesImages
        ) = await self.crawler.getTabContent(url=URL+"NewReleases", divId="NewReleasesRows")

        await self.sendGameTabToUser(
            ctx=ctx,
            gamesNames=gamesNames,
            gamesUrls=gamesUrls,
            gamesOriginalPrices=gamesOriginalPrices,
            gamesFinalPrices=gamesFinalPrices
        )
    
    @gameTab.command(
        name="mais vendidos", 
        aliases=[
            "maisvendidos",
            "mv"
        ]
    )
    async def topSellers(self, ctx: Context):
        (
            gamesNames, 
            gamesUrls, 
            gamesOriginalPrices, 
            gamesFinalPrices, 
            gamesImages
        ) = await self.crawler.getTabContent(url=URL+"TopSellers", divId="TopSellersRows")

        await self.sendGameTabToUser(
            ctx=ctx,
            gamesNames=gamesNames,
            gamesUrls=gamesUrls,
            gamesOriginalPrices=gamesOriginalPrices,
            gamesFinalPrices=gamesFinalPrices
        )

    @gameTab.command(
        name="jogos populares", 
        aliases=[
            "jogospopulares",
            "jp"
        ]
    )
    async def beingPlayed(self, ctx: Context):
        (
            gamesNames, 
            gamesUrls, 
            gamesOriginalPrices, 
            gamesFinalPrices, 
            gamesImages
        ) = await self.crawler.getTabContent(url=URL+"ConcurrentUsers", divId="ConcurrentUsersRows")

        await self.sendGameTabToUser(
            ctx=ctx,
            gamesNames=gamesNames,
            gamesUrls=gamesUrls,
            gamesOriginalPrices=gamesOriginalPrices,
            gamesFinalPrices=gamesFinalPrices
        )

    @gameTab.command(
        name="pré-venda", 
        aliases=[
            "pré venda",
            "prévenda",
            "pre-venda",
            "pre venda",
            "prevenda",
            "pv"
        ]
    )
    async def prePurchase(self, ctx: Context):
        (
            gamesNames, 
            gamesUrls, 
            gamesOriginalPrices, 
            gamesFinalPrices, 
            gamesImages
        ) = await self.crawler.getTabContent(url=URL+"ComingSoon", divId="ComingSoonRows")

        await self.sendGameTabToUser(
            ctx=ctx,
            gamesNames=gamesNames,
            gamesUrls=gamesUrls,
            gamesOriginalPrices=gamesOriginalPrices,
            gamesFinalPrices=gamesFinalPrices
        )

    async def sendGameTabToUser(
        self, 
        ctx: Context, 
        gamesNames: list, 
        gamesUrls: list, 
        gamesOriginalPrices: list, 
        gamesFinalPrices: list
    ) -> None:
        """ Envia para o usuário o resultado dos jogos das tabelas encontradas.

        Parameters
        -----------
        ctx: :class:`Context`
            Contexto da mensagem
        gamesNames: :class:`list`
            Lista com os nomes do jogos.
        gamesUrls: :class:`list`
            Lista com as URLs dos jogos
        gamesOriginalPrices: :class:`list`
            Lista com os preços originais dos jogos
        gamesFinalPrices: :class:`list`
            Lista com os preços com desconto dos jogos

        """

        if(
            gamesNames != None and 
            gamesUrls != None and 
            gamesOriginalPrices != None and 
            gamesFinalPrices != None
        ):
            gamesNames.reverse() 
            gamesUrls.reverse() 
            gamesOriginalPrices.reverse() 
            gamesFinalPrices.reverse()
            
            num = x = len(gamesNames)

            if(x == 0):
                await ctx.send(self.message.noOffers()[1])
            else:
                messageConcat0 = ""
                messageConcat1 = ""
                member         = ctx.author
                
                while(x > 0):
                    if(x >= (num/2)):
                        messageConcat0 = messageConcat0 + "**Nome: **" + \
                            gamesNames[x - 1] + "\n**Link:** <" + \
                            gamesUrls[x - 1] + ">" + "\n**Preço Original: **" + \
                            gamesOriginalPrices[x - 1] + "\n**Preço com Desconto: **" + \
                            gamesFinalPrices[x - 1] + "\n\n"
                    else:
                        messageConcat1 = messageConcat1 + "**Nome: **" + \
                            gamesNames[x - 1] + "\n**Link:** <" + \
                            gamesUrls[x - 1] + ">" + "\n**Preço Original: **" + \
                            gamesOriginalPrices[x - 1] + "\n**Preço com Desconto: **" + \
                            gamesFinalPrices[x - 1] + "\n\n"
                    
                    x -= 1

                await ctx.send(member.mention + self.message.checkDm())
                
                await member.send(messageConcat0)
                await member.send(messageConcat1)
        else:
            await ctx.send(self.message.somethingWentWrong()[0])
    
    @commands.command(name="game", aliases=["jogo"])
    async def specificGame(self, ctx: Context, *, args: str):
        gameToSearch = args

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
            gameToSearch = gameToSearch
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
                await ctx.send(self.message.commandAlert(self.prefix)[0])

    @commands.command(name="genre", aliases=["gênero", "genero"])
    async def gameGenre(self, ctx: Context, *, args: str):
        gameGenreToSearch = args

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
            gameOriginalPrice , 
            gameFinalPrice, 
            gameIMG
        ) = await self.crawler.getGameRecommendationByGenre(gameGenreToSearch)

        if(gameName != None):
            embedGameRecommendationByGenre = Embed(
                title = self.message.title(genre=gameGenreToSearch)[6],
                color = self.color
            )
            embedGameRecommendationByGenre.set_image(url=gameIMG)
            embedGameRecommendationByGenre.add_field(
                name   = "**Nome:**", 
                value  = "**{}**".format(gameName), 
                inline = False
            )
            embedGameRecommendationByGenre.add_field(
                name   = "**Link:**", 
                value  = "**[Clique Aqui]({})**".format(gameURL), 
                inline = False
            )

            if(
                (gameOriginalPrice == gameFinalPrice) and 
                (gameOriginalPrice != "Gratuito p/ Jogar")
            ):
                embedGameRecommendationByGenre.add_field(
                    name   = "**Preço:**", 
                    value  = "**{}**".format(gameOriginalPrice), 
                    inline = True
                )
            else:
                if(gameOriginalPrice != "Gratuito p/ Jogar"):
                    embedGameRecommendationByGenre.add_field(
                        name   = "**Preço Original:**", 
                        value  = "**{}**".format(gameOriginalPrice), 
                        inline = True
                    )
                    embedGameRecommendationByGenre.add_field(
                        name   = "**Preço com Desconto:**", 
                        value  = "**{}**".format(gameFinalPrice), 
                        inline = True
                    )
                else:
                    embedGameRecommendationByGenre.add_field(
                        name   = "**Preço:**", 
                        value  = "**{}**".format(gameOriginalPrice), 
                        inline = True
                    )

            await searchGenreMessage.edit(content="", embed=embedGameRecommendationByGenre)
            await searchGenreMessage.add_reaction(self.reactions[0])
        else:
            await searchGenreMessage.edit(content=self.message.noOffers(prefix=self.prefix)[3])

    @gameGenre.error
    async def gameGenreError(self, ctx: Context, error: CommandError):
        if(isinstance(error, commands.MissingRequiredArgument)):
            if(error.param.name == "args"):
                await ctx.send(self.message.commandAlert(self.prefix)[1])

    @commands.command(name="maxprice", aliases=["preço máximo"])
    async def maxPrice(self, ctx: Context, *, args: str):
        if(not args.isnumeric()):
            raise commands.ArgumentParsingError()
        
        maxPrice = args

        # Mensagem de busca de jogo, com efeito de carregamento.
        messageContent    = self.message.searchMessage()[3]
        searchGameMessage = await ctx.send(messageContent + " "+ maxPrice + "__ .**")
        
        sleep(0.5)
        await searchGameMessage.edit(content=messageContent + " " + maxPrice + "__ . .**")
        
        sleep(0.5)
        await searchGameMessage.edit(content=messageContent + " "+ maxPrice + "__ . . .**")

        if(float(maxPrice) > 120):
            maxPriceCode = "rZ04j" # Preço maior que R$ 120,00
        elif(float(maxPrice) < 10):
            maxPriceCode = "19Jfc" # Preço menor que R$ 10,00
        else:
            maxPriceCode = None
        
        (
            gameName,
            gameIMG, 
            gameURL, 
            gameOriginalPrice,
            gameFinalPrice
        ) = await self.crawler.getGameRecommendationByPriceRange(code=maxPriceCode, maxPrice=float(maxPrice))

        embedGameRecommendationByPrice = Embed(
            title = self.message.title(gameName=gameName)[7],
            color = self.color
        )
        embedGameRecommendationByPrice.set_image(url=gameIMG)
        embedGameRecommendationByPrice.add_field(
            name   = "**Link:**", 
            value  = "**[Clique Aqui]({})**".format(gameURL), 
            inline = False
        )
        
        if(gameOriginalPrice != gameFinalPrice): # Caso o jogo esteja em promoção.
            embedGameRecommendationByPrice.add_field(
                name   = "**Preço Original:**", 
                value  = "**{}**".format(gameOriginalPrice), 
                inline = True
            )
            embedGameRecommendationByPrice.add_field(
                name   = "**Preço com Desconto:**", 
                value  = "**{}**".format(gameFinalPrice), 
                inline = True
            )
        else: # Caso o jogo não esteja em promoção.
            embedGameRecommendationByPrice.add_field(
                name   = "**Preço:**", 
                value  = "**{}**".format(gameOriginalPrice), 
                inline = False
            )

        if(maxPriceCode == "rZ04j"):
            embedGameRecommendationByPrice.set_footer(
                text = self.message.recommendationByPrice()[1]
            )
        elif(maxPriceCode == "19Jfc"):
            embedGameRecommendationByPrice.set_footer(
                text = self.message.recommendationByPrice()[2]
            )
        
        await searchGameMessage.edit(content="", embed=embedGameRecommendationByPrice)
        await searchGameMessage.add_reaction(self.reactions[0])
        
    @maxPrice.error
    async def maxPriceError(self, ctx: Context, error: CommandError):
        if(isinstance(error, commands.MissingRequiredArgument)):
            if(error.param.name == "args"):
                await ctx.send(self.message.recommendationByPrice()[3])
        if(isinstance(error, commands.ArgumentParsingError)):
            await ctx.send(self.message.recommendationByPrice()[0])
    
    @commands.command(
        name="review", 
        aliases=["reviews", "análise", "análises", "analise", "analises"]
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

        # Caso seja passado o link do jogo.
        if(gameToSearch.lower().find("store.steampowered.com/app") != -1):
            (
                gameName, 
                gameIMG, 
                gameOriginalPrice,
                gameFinalPrice,
                gameDescription
            ) = await self.crawler.getGameByLink(gameToSearch)

            searchUrl = None
            gameURL   = gameToSearch + "?l=brazilian"
        else: # Caso seja passado o nome do jogo.
            (
                gameName, 
                gameURL, 
                gameIMG, 
                gameOriginalPrice,
                gameFinalPrice,
                searchUrl,
                gameDescription
            ) = await self.crawler.getSpecificGame(gameToSearch)

        if(gameURL != None):
            embedGameReview = await gameReviewEmbed(
                crawler    = self.crawler,
                embedColor = self.color,
                gameUrl    = gameURL,
                gameName   = gameName,
                gameIMG    = gameIMG,
                searchUrl  = searchUrl
            )

            await searchMessage.edit(content="", embed=embedGameReview)
            await searchMessage.add_reaction(self.reactions[1])
        else:
            await searchMessage.edit(content=self.message.noOffers()[2])

    @review.error
    async def reviewError(self, ctx: Context, error: CommandError):
        if(isinstance(error, commands.MissingRequiredArgument)):
            if(error.param.name == "args"):
                await ctx.send(self.message.commandAlert(self.prefix)[4])

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