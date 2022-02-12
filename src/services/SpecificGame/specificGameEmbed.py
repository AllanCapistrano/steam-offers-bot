from typing import Literal
from discord.embeds import Embed

from services.crawler import Crawler
from services.messages import Message
from embeds.embedSpecificGame import EmbedSpecificGame

async def specificGameEmbed(
    crawler: Crawler,
    embedColor: Literal,
    gameToSearch: str,
    language: str = None
) -> Embed:
    """ Função responsável por montar a Embed de um jogo específico.

    Parametrs
    ----------
    crawler: :class:`Crawler`
    embedColor: :class:`Literal`
    gameToSearch :class:`str`
    language :class:`str`

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

        if(language == None):
            gameURL = gameToSearch + "?l=brazilian"
        elif(language == "en"):
            gameURL = gameToSearch + "?l=english"
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
        embedSpecificGame = EmbedSpecificGame(
            color             = embedColor,
            gameName          = gameName,
            gameImg           = gameIMG,
            gameUrl           = gameURL,
            gameOriginalPrice = gameOriginalPrice,
            gameFinalPrice    = gameFinalPrice,
            gameDescription   = gameDescription,
            searchUrl         = searchUrl,
            message           = Message()
        )

        if(language == "en"):
            return embedSpecificGame.embedSpecificGameEnglish()

        return embedSpecificGame.embedSpecificGamePortuguese()
    else:
        return None