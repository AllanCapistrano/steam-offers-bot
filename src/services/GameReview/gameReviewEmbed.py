from typing import Literal
from discord.embeds import Embed

from services.crawler import Crawler
from services.messages import Message
from embeds.embedGameReview import EmbedGameReview

async def gameReviewEmbed(
    crawler: Crawler,
    embedColor: Literal,
    gameUrl: str, 
    gameName: str, 
    gameIMG: str,
    searchUrl: str
) -> Embed:
    """ Função responsável por montar a Embed de análises dos jogos.

    Parameters
    -----------
    crawler: :class:`Crawler`
    embedColor: :class:`Literal`
    gameUrl: :class:`str`
    gameName: :class:`str`
    gameIMG: :class:`str`
    searchUrl: :class:`str`

    Returns
    -----------
    embedGameReview: :class:`Embed`
    """
    
    (
        sumary, 
        totalAmount
    ) = await crawler.getGameReview(gameUrl)

    embedGameReview = EmbedGameReview(
        color       = embedColor,
        gameName    = gameName,
        gameImg     = gameIMG,
        searchUrl   = searchUrl,
        sumary      = sumary,
        totalAmount = totalAmount,
        message     = Message()
    )

    return embedGameReview.embedGameReviewPortuguese()