from typing import Literal

from discord.ext import commands
from discord.ext.commands import Bot, Context

from services.crawler import Crawler
from services.messages import Message
from services.currency import Currency

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
        self.currency  = Currency()
        self.imgGenre  = IMG_GENRES
        self.url       = URL

    async def sendGameTabToUser(
        self, 
        ctx: Context, 
        gamesNames: list, 
        gamesUrls: list, 
        gamesOriginalPrices: list, 
        gamesFinalPrices: list,
        language: str = None
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
        language: :class:`str`
            Idioma do comando.

        """

        if(
            gamesNames          != None and 
            gamesUrls           != None and 
            gamesOriginalPrices != None and 
            gamesFinalPrices    != None
        ):
            gamesNames.reverse() 
            gamesUrls.reverse() 
            gamesOriginalPrices.reverse() 
            gamesFinalPrices.reverse()
            
            num = x = len(gamesNames)

            if(
                len(gamesNames)          == 0 or
                len(gamesUrls)           == 0 or
                len(gamesOriginalPrices) == 0 or
                len(gamesFinalPrices)    == 0
            ):
                if(language == None):
                    await ctx.send(self.message.noOffers()[1])
                if(language == "en"):
                    await ctx.send(self.message.noOffers(language="en")[1])
            else:
                messageConcat0 = ""
                messageConcat1 = ""
                member         = ctx.author
                
                if(language == None):
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
                elif(language == "en"):
                    while(x > 0):
                        if(x >= (num/2)):
                            messageConcat0 = messageConcat0 + "**Name: **" + \
                                gamesNames[x - 1] + "\n**Link:** <" + \
                                gamesUrls[x - 1] + ">" + "\n**Original Price: **" + \
                                gamesOriginalPrices[x - 1] + "\n**Discount Price: **" + \
                                gamesFinalPrices[x - 1] + "\n\n"
                        else:
                            messageConcat1 = messageConcat1 + "**Name: **" + \
                                gamesNames[x - 1] + "\n**Link:** <" + \
                                gamesUrls[x - 1] + ">" + "\n**Original Price: **" + \
                                gamesOriginalPrices[x - 1] + "\n**Discount Price: **" + \
                                gamesFinalPrices[x - 1] + "\n\n"
                        
                        x -= 1

                    await ctx.send(member.mention + self.message.checkDm(language="en"))
                
                await member.send(messageConcat0)
                await member.send(messageConcat1)
        else:
            if(language == None):
                await ctx.send(self.message.somethingWentWrong()[0])
            if(language == "en"):
                await ctx.send(self.message.somethingWentWrong(language="en")[0])