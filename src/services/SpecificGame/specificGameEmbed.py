from typing import Literal
from discord.embeds import Embed

from services.crawler import Crawler
from services.messages import Message
from embeds.embedSpecificGame import EmbedSpecificGame

async def specificGameEmbed(
    crawler: Crawler,
    embedColor: Literal,
    gameToSearch: str,
    currency: str,
    language: str
) -> Embed:
    """ Função responsável por montar a Embed de um jogo específico.

    Parametrs
    ----------
    crawler: :class:`Crawler`
        Crawler para realizar as buscas.
    embedColor: :class:`Literal`
        Cor utilizada para customizar a Embed.
    gameToSearch :class:`str`
        Jogo que se deseja buscar, pode ser tanto o nome quando o link da 
        página do jogo na Steam.
    currency: :class:`str`
        Moeda que se deseja ver o preço.
    language: :class:`str`
        Linguagem que se deseja visualizar a página do jogo.

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
            gameURL = gameToSearch + f"?l=brazilian"
        else:
            gameURL = gameToSearch + f"?l={language}"
    else:
        (
            gameName, 
            gameURL, 
            gameIMG, 
            gameOriginalPrice,
            gameFinalPrice,
            searchUrl,
            gameDescription
        ) = await crawler.getSpecificGame(
                gameName = gameToSearch,
                currency = currency,
                language = language
            )

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

        if(language == "english"):
            return embedSpecificGame.embedSpecificGameEnglish()

        return embedSpecificGame.embedSpecificGamePortuguese()
    else:
        return None