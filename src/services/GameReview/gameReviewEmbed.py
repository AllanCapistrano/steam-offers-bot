from typing import Literal
from discord.embeds import Embed

from services.crawler import Crawler
from services.messages import Message
from embeds.embedGameReview import EmbedGameReview

async def gameReviewEmbed(
    crawler: Crawler,
    embedColor: Literal,
    gameToSearch: str, 
    language: str = None
) -> Embed:
    """ Função responsável por montar a Embed de análises dos jogos.

    Parameters
    -----------
    crawler: :class:`Crawler`
    embedColor: :class:`Literal`
    gameToSearch: :class:`str`
    language: :class:`str`

    Returns
    -----------
    embedGameReview: :class:`Embed`
    """
    
    if(gameToSearch.lower().find("store.steampowered.com/app") != -1):
        (
            gameName, 
            gameIMG, 
            gameOriginalPrice,
            gameFinalPrice,
            gameDescription
        ) = await crawler.getGameByLink(
                url      = gameToSearch,
                language = language
            )

        searchUrl = None

        if(language == None):
            gameURL = gameToSearch + "?l=brazilian"
        else:
            gameURL = gameToSearch + f"?l={language}"
        
    else: # Caso seja passado o nome do jogo.
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
                language = language
            )

    if(
        gameURL   != None and
        gameIMG   != None and
        gameName  != None 
    ):
        if(language == None):
            gameURL = gameURL + "&l=brazilian"
        else:
            gameURL = gameURL + f"&l={language}"

        (
            summary, 
            totalAmount
        ) = await crawler.getGameReview(gameURL)

        embedGameReview = EmbedGameReview(
            color       = embedColor,
            gameName    = gameName,
            gameImg     = gameIMG,
            searchUrl   = searchUrl,
            summary     = summary,
            totalAmount = totalAmount,
            message     = Message()
        )

        if(language == "english"):
            return embedGameReview.embedGameReviewEnglish()
        
        return embedGameReview.embedGameReviewPortuguese()
    else:
        return None