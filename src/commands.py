from time import sleep
from typing import Literal

from discord import Embed
from discord.ext import commands
from discord.ext.commands import Bot

from services.crawler import Crawler
from services.messages import Message

# ------------------------------ Constants ----------------------------------- #
IMG_GENRES = "https://i.imgur.com/q0NfeWX.png"
# ---------------------------------------------------------------------------- #

class Commands(commands.Cog):
    def __init__(
        self, 
        client: Bot, 
        prefix: str, 
        color: Literal, 
        urlInvite: str,
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
                name   = "```{0}novidades``` ou ```{0}populares``` ou ```{0}np```".format(self.prefix),
                value  = self.message.helpValues()[3], 
                inline = False
            )
            embedHelp.add_field(
                name   = "```{0}mais vendidos``` ou ```{0}mv```".format(self.prefix),
                value  = self.message.helpValues()[4], 
                inline = False
            )
            embedHelp.add_field(
                name   = "```{0}jogos populares``` ou ```{0}jp```".format(self.prefix),
                value  = self.message.helpValues()[5], 
                inline = False
            )
            embedHelp.add_field(
                name   = "```{0}pré-venda``` ou ```{0}pv```".format(self.prefix),
                value  = self.message.helpValues()[6], 
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
        else:
            # DISPARAR MENSAGEM DE COMANDO INVÁLIDO!
            print("Comando errado!")

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