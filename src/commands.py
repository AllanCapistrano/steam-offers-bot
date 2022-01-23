from time import sleep
from typing import Literal

from discord import Embed
from discord.ext import commands
from discord.ext.commands import Bot

from services.crawler import Crawler
from services.messages import Message
from services.SpecificGame.specificGameEmbed import specificGameEmbed
from services.GameReview.gameReviewEmbed import gameReviewEmbed

# ------------------------------ Constants ----------------------------------- #
IMG_GENRES = "https://i.imgur.com/q0NfeWX.png"
URL        = "https://store.steampowered.com/specials?cc=br#p=0&tab="
# ---------------------------------------------------------------------------- #

class Commands(commands.Cog):
    def __init__(
        self, 
        client: Bot, 
        prefix: str, 
        color: Literal, 
        urlInvite: str,
        ownerId: str,
        reactions: list
    ) -> None:
        """ Método construtor.

        Parameters
        -----------
        client: :class:`Bot`
        color: :class:`Literal`
        urlInvite: :class:`str`
        message: :class:`Message`
        """
    
        self.client    = client
        self.prefix    = prefix
        self.color     = color
        self.urlInvite = urlInvite
        self.ownerId   = ownerId
        self.reactions = reactions
        self.message   = Message()
        self.crawler   = Crawler()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"\nO {self.client.user.name} está escutando os comandos.")

    @commands.command(name="help", aliases=["ajuda", "comandos"])
    async def help(self, ctx, *args):
        if(len(args) == 0):
            embedHelp = Embed(
                color = self.color
            )
            embedHelp.set_author(
                name     = f"{self.client.user.name} lista de comandos:", 
                icon_url = self.client.user.avatar_url
            )
            embedHelp.add_field(
                name   = "```{0}promoção``` ou ```{0}pr```".format(self.prefix),
                value  = self.message.helpValues()[1], 
                inline = False
            )
            embedHelp.add_field(
                name   = "```{0}destaque``` ou ```{0}dt```".format(self.prefix),
                value  = self.message.helpValues()[2], 
                inline = False
            )
            embedHelp.add_field(
                name   = "```{0}gametab [categoria]```".format(self.prefix),
                value  = self.message.helpValues(prefix=self.prefix)[13], 
                inline = False
            )
            embedHelp.add_field(
                name   = "```{}convite```".format(self.prefix),
                value  = self.message.helpValues()[7], 
                inline = False
            )
            embedHelp.add_field(
                name   = "```{}botinfo```".format(self.prefix),
                value  = self.message.helpValues()[8], 
                inline = False
            )
            embedHelp.add_field(
                name   = "```{}game [nome do jogo]```".format(self.prefix),
                value  = self.message.helpValues()[9], 
                inline = False
            )
            embedHelp.add_field(
                name   = "```{}genre [gênero do jogo]```".format(self.prefix),
                value  = self.message.helpValues()[10], 
                inline = False
            )
            embedHelp.add_field(
                name   = "```{}maxprice [preço]```".format(self.prefix),
                value  = self.message.helpValues()[11], 
                inline = False
            )
            embedHelp.add_field(
                name   = "```{0}análises [nome do jogo]``` ou ```{0}reviews [nome do jogo]```".format(self.prefix),
                value  = self.message.helpValues()[12], 
                inline = False
            )

            await ctx.send(embed=embedHelp)
        elif(len(args) == 1 and args[0] == "genre"):
            embedHelp = Embed(
                title = self.message.title()[4],
                color = self.color,
                description = self.message.gameGenres()
            )
            embedHelp.add_field(
                name   = "Ficou confuso(a) ?",
                value  = self.message.helpValues(img=IMG_GENRES)[0],
                inline = False
            )
            embedHelp.set_footer(text="Utilize {}genre [um dos gêneros acima]".format(self.prefix))

            await ctx.send(embed=embedHelp)
        elif(len(args) == 1 and args[0] == "gametab"):
            embedHelp = Embed(
                color = self.color
            )
            embedHelp.set_author(
                name     = f"{self.client.user.name} comando {self.prefix}gametab:", 
                icon_url = self.client.user.avatar_url
            )
            embedHelp.add_field(
                name   = "```{0}gametab novidades populares``` ou ```{0}gametab np```".format(self.prefix),
                value  = self.message.helpValues()[3], 
                inline = False
            )
            embedHelp.add_field(
                name   = "```{0}gametab mais vendidos``` ou ```{0}gametab mv```".format(self.prefix),
                value  = self.message.helpValues()[4], 
                inline = False
            )
            embedHelp.add_field(
                name   = "```{0}gametab jogos populares``` ou ```{0}gametab jp```".format(self.prefix),
                value  = self.message.helpValues()[5], 
                inline = False
            )
            embedHelp.add_field(
                name   = "```{0}gametab pré-venda``` ou ```{0}gametab pv```".format(self.prefix),
                value  = self.message.helpValues()[6], 
                inline = False
            )
            await ctx.send(embed=embedHelp)
        else:
            # Do something
            print("Comando inválido!")

    @commands.command(name="invite", aliases=["convite"])
    async def invite(self, ctx):
        embedInvite = Embed(
            title       = self.message.title()[0],
            color       = self.color,
            description = f"**{self.urlInvite}**",
        )
        embedInvite.set_thumbnail(url=self.client.user.avatar_url)

        await ctx.send(embed=embedInvite)

    @commands.command(name="destaque", aliases=["dt"])
    async def spotlightOffers(self, ctx):
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
    async def dailyGamesOffers(self, ctx):
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

        if(x == 0):
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
    async def botInfo(self, ctx):
        embedBotInfo = Embed(
            title = self.message.title()[3],
            color = self.color
        )
        embedBotInfo.set_thumbnail(url=self.client.user.avatar_url)
        embedBotInfo.add_field(
            name   = "Python", 
            value  = self.message.infoValues()[0], 
            inline = True
        )
        embedBotInfo.add_field(
            name   = "discord.py", 
            value  = self.message.infoValues()[1], 
            inline = True
        )
        embedBotInfo.add_field(
            name   = "Sobre {}".format(self.client.user.name), 
            value  = self.message.infoValues()[2] + 
            self.client.get_user(self.ownerId).name + "#" 
            + self.client.get_user(self.ownerId).discriminator + "**", 
            inline = False
        )
        embedBotInfo.set_author(
            name     = self.client.get_user(self.ownerId).name + "#" 
            + self.client.get_user(self.ownerId).discriminator, 
            icon_url = self.client.get_user(self.ownerId).avatar_url
        )
        embedBotInfo.set_footer(
            text="Criado em 26 de Maio de 2020! | Última atualização em {}."
            .format(self.message.infoValues()[3])
        )

        await ctx.send(embed=embedBotInfo)

    @commands.command(name="gametab")
    async def newReleases(self, ctx, *args):
        if(len(args) == 0):
            await ctx.send(self.message.commandAlert(prefix=self.prefix)[3])
        else:
            command = ""

            for arg in args:
                command += arg

            gamesNames          = None
            gamesUrls           = None
            gamesOriginalPrices = None
            gamesFinalPrices    = None

            match command:
                case (
                    "novidades populares" | 
                    "novidadespopulares" |
                    "novidades" | 
                    "populares" | 
                    "np"
                ):
                    (
                        gamesNames, 
                        gamesUrls, 
                        gamesOriginalPrices, 
                        gamesFinalPrices, 
                        gamesImages
                    ) = await self.crawler.getTabContent(url=URL+"NewReleases", divId="NewReleasesRows")
                case ("mais vendidos" | "maisvendidos" | "mv"):
                    (
                        gamesNames, 
                        gamesUrls, 
                        gamesOriginalPrices, 
                        gamesFinalPrices, 
                        gamesImages
                    ) = await self.crawler.getTabContent(url=URL+"TopSellers", divId="TopSellersRows")
                case ("jogos populares" | "jogospopulares" | "jp"):
                    (
                        gamesNames, 
                        gamesUrls, 
                        gamesOriginalPrices, 
                        gamesFinalPrices, 
                        gamesImages
                    ) = await self.crawler.getTabContent(url=URL+"ConcurrentUsers", divId="ConcurrentUsersRows")
                case (
                    "pré-venda" | 
                    "pré venda" | 
                    "prévenda" | 
                    "pre-venda" | 
                    "pre venda" | 
                    "prevenda" | 
                    "pv"
                ):
                    (
                        gamesNames, 
                        gamesUrls, 
                        gamesOriginalPrices, 
                        gamesFinalPrices, 
                        gamesImages
                    ) = await self.crawler.getTabContent(url=URL+"ComingSoon", divId="ComingSoonRows")
                case _:
                    await ctx.send(
                        self.message.commandAlert()[2] + 
                        f"\nDigite **{self.prefix}help gametab** para ver todas as possibilidades"
                    )
        
            if(
                gamesNames != None or 
                gamesUrls != None or 
                gamesOriginalPrices != None or 
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

    @commands.command(name="game", aliases=["jogo"])
    async def specificGame(self, ctx, *args):
        if(len(args) == 0):
            await ctx.send(self.message.commandAlert(prefix=self.prefix)[0])
        else:
            gameToSearch = ""

            for arg in args:
                gameToSearch += arg

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

    @commands.command(name="genre", aliases=["gênero", "genero"])
    async def gameGenre(self, ctx, *args):
        if(len(args) == 0):
            await ctx.send(self.message.commandAlert(prefix=self.prefix)[1])
        else:
            gameGenreToSearch = ""

            for arg in args:
                gameGenreToSearch += arg

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

