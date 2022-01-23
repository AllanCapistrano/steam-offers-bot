from typing import Literal
import discord
from discord.embeds import Embed

from services.crawler import Crawler
from services.messages import Message

async def specificGameEmbed(
    crawler: Crawler,
    embedColor: Literal,
    gameToSearch: str
) -> Embed:
    """ Função responsável por montar a Embed de um jogo específico.

    Parametrs
    ----------
    crawler: :class:`Crawler`
    embedColor: :class:`Literal`
    gameToSearch :class:`str`

    Returns
    ----------
    embedSpecificGame: :class:`Embed`
    """

    if(gameToSearch.lower().find("store.steampowered.com/app") != -1):
        (
            gameName, 
            gameIMG, 
            gameOriginalPrice,
            gameFinalPrice,
            gameDescription
        ) = await crawler.getGameByLink(gameToSearch)

        searchUrl = None
        gameURL   = gameToSearch + "?l=brazilian"
    else:
        (
            gameName, 
            gameURL, 
            gameIMG, 
            gameOriginalPrice,
            gameFinalPrice,
            searchUrl,
            gameDescription
        ) = await crawler.getSpecificGame(gameToSearch)

    if(
        gameName          != None and
        gameURL           != None and
        gameIMG           != None and
        gameOriginalPrice != None and
        gameFinalPrice    != None
    ):
        message = Message()

        embedSpecificGame = discord.Embed(
            title = message.title(gameName=gameName)[5],
            color = embedColor
        )
        embedSpecificGame.set_image(url=gameIMG)
        embedSpecificGame.add_field(
            name   = "**Link:**", 
            value  = "**[Clique Aqui]({})**".format(gameURL), 
            inline = False
        )

        if(gameOriginalPrice != gameFinalPrice): # Caso o jogo esteja em promoção.
            embedSpecificGame.add_field(
                name   = "**Preço Original:**", 
                value  = "**{}**".format(gameOriginalPrice), 
                inline = True
            )
            embedSpecificGame.add_field(
                name   = "**Preço com Desconto:**", 
                value  = "**{}**".format(gameFinalPrice), 
                inline = True
            )
        else: # Caso o jogo não esteja em promoção.
            embedSpecificGame.add_field(
                name   = "**Preço:**", 
                value  = "**{}**".format(gameOriginalPrice), 
                inline = False
            )

        if(gameDescription != None):
            embedSpecificGame.add_field(
                name   = "**Descrição:**", 
                value  = "{}".format(gameDescription), 
                inline = False
            )

        if(searchUrl != None): # Caso seja passado o nome do jogo.
            embedSpecificGame.add_field(
                name   = "**Obs:**", 
                value  = message.wrongGame(searchUrl), 
                inline = False
            )

        return embedSpecificGame
    else:
        return None