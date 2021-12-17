from typing import Literal
import discord
from discord.embeds import Embed

from services.crawler import Crawler
from services import messages

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
    ) = await crawler.getGameReviews(gameUrl)

    if (sumary[0].find("positivas") != -1):
        embedGameReview = discord.Embed(
            title = "👍 Jogo: {} 👍".format(gameName),
            color = embedColor
        )
    elif(sumary[0].find("negativas") != -1):
        embedGameReview = discord.Embed(
            title = "👎 Jogo: {} 👎".format(gameName),
            color = embedColor
        )
    else:
        embedGameReview = discord.Embed(
            title = "👍 Jogo: {} 👎".format(gameName),
            color = embedColor
        )
    
    embedGameReview.set_image(url=gameIMG)

    if(len(sumary) == 1 and len(totalAmount) == 1):
        embedGameReview.add_field(
            name   = "**Todas as análises:**", 
            value  = "{} (Qtd. de análises: {})".format(sumary[0], totalAmount[0]), 
            inline = False
        ) 
    elif(len(sumary) == 2 and len(totalAmount) == 2):
        embedGameReview.add_field(
            name   = "**Análises Recentes:**", 
            value  = "{} (Qtd. de análises: {})".format(sumary[0], totalAmount[0]), 
            inline = False
        )
        embedGameReview.add_field(
            name   = "**Todas as análises:**", 
            value  = "{} (Qtd. de análises: {})".format(sumary[1], totalAmount[1]), 
            inline = False
        )

    embedGameReview.add_field(
        name   = "**Obs:**", 
        value  = messages.wrongGame(searchUrl), 
        inline = False
    )

    return embedGameReview