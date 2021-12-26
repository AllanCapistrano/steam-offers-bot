from typing import Literal
import discord
from discord.embeds import Embed

from services.crawler import Crawler
from services import messages

async def specificGameEmbed(
    crawler: Crawler,
    embedColor: Literal,
    gameNameToSearch: str
) -> Embed:
    """ Função responsável por montar a Embed de um jogo específico.

    Parametrs
    ----------
    crawler: :class:`Crawler`
    embedColor: :class:`Literal`
    gameNameToSearch :class:`str`

    Returns
    ----------
    embedSpecificGame: :class:`Embed`
    """
    
    (
        gameName, 
        gameURL, 
        gameIMG, 
        gameOriginalPrice,
        gameFinalPrice,
        searchUrl,
        gameDescription
    ) = await crawler.getSpecificGame(gameNameToSearch)

    if(gameName != None):
        embedSpecificGame = discord.Embed(
            title = messages.title(gameName=gameName)[5],
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

        embedSpecificGame.add_field(
            name   = "**Obs:**", 
            value  = messages.wrongGame(searchUrl), 
            inline = False
        )

        return embedSpecificGame
    else:
        return None