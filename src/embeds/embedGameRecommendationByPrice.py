from typing import Literal

from discord import Embed

from services.messages import Message

class EmbedGameRecommendationByPrice():
    def __init__(
        self,
        color: Literal, 
        gameName: str,
        gameImg: str,
        gameUrl: str,
        gameOriginalPrice: str,
        gameFinalPrice: str,
        maxPriceCode: str,
        message: Message,
    ) -> None:
        """ Método construtor.

        Parameters
        -----------
        color: :class:`Literal`
        gameName: :class:`str`
        gameImg: :class:`str`
        gameUrl: :class:`str`
        gameOriginalPrice: :class:`str`
        gameFinalPrice: :class:`str`
        maxPriceCode: :class:`str`
        message: :class:`Message`
        """
        
        self.color             = color
        self.gameName          = gameName
        self.gameImg           = gameImg
        self.gameUrl           = gameUrl
        self.gameOriginalPrice = gameOriginalPrice
        self.gameFinalPrice    = gameFinalPrice
        self.maxPriceCode      = maxPriceCode
        self.message           = message
        self.embed             = Embed(color=self.color)

    def embedSpecificGamePortuguese(self) -> Embed:
        """ Monta a Embed do comando de recomendação de jogo por faixa de preço 
        em Português.

        Returns
        -----------
        embed: :class:`Embed`
        """

        self.embed.title = self.message.title(gameName=self.gameName)[7]

        self.embed.set_image(url=self.gameImg)
        self.embed.add_field(
            name   = "**Link:**", 
            value  = "**[Clique Aqui]({})**".format(self.gameUrl), 
            inline = False
        )
        
        # Caso o jogo esteja em promoção.
        if(self.gameOriginalPrice != self.gameFinalPrice):
            self.embed.add_field(
                name   = "**Preço Original:**", 
                value  = "**{}**".format(self.gameOriginalPrice), 
                inline = True
            )
            self.embed.add_field(
                name   = "**Preço com Desconto:**", 
                value  = "**{}**".format(self.gameFinalPrice), 
                inline = True
            )
        else: # Caso o jogo não esteja em promoção.
            self.embed.add_field(
                name   = "**Preço:**", 
                value  = "**{}**".format(self.gameOriginalPrice), 
                inline = False
            )

        if(self.maxPriceCode == "rZ04j"):
            self.embed.set_footer(
                text = self.message.recommendationByPrice()[1]
            )
        elif(self.maxPriceCode == "19Jfc"):
            self.embed.set_footer(
                text = self.message.recommendationByPrice()[2]
            )

        return self.embed

    def embedSpecificGameEnglish(self) -> Embed:
        """ Monta a Embed do comando de recomendação de jogo por faixa de preço 
        em Inglês.

        Returns
        -----------
        embed: :class:`Embed`
        """

        self.embed.title = self.message.title(
            language = "en",
            gameName = self.gameName
        )[7]

        self.embed.set_image(url=self.gameImg)
        self.embed.add_field(
            name   = "**Link:**", 
            value  = "**[Click Here]({})**".format(self.gameUrl), 
            inline = False
        )
        
        # Caso o jogo esteja em promoção.
        if(self.gameOriginalPrice != self.gameFinalPrice):
            self.embed.add_field(
                name   = "**Original Price:**", 
                value  = "**{}**".format(self.gameOriginalPrice), 
                inline = True
            )
            self.embed.add_field(
                name   = "**Discount Price:**", 
                value  = "**{}**".format(self.gameFinalPrice), 
                inline = True
            )
        else: # Caso o jogo não esteja em promoção.
            self.embed.add_field(
                name   = "**Price:**", 
                value  = "**{}**".format(self.gameOriginalPrice), 
                inline = False
            )

        if(self.maxPriceCode == "rZ04j"):
            self.embed.set_footer(
                text = self.message.recommendationByPrice(language="en")[1]
            )
        elif(self.maxPriceCode == "19Jfc"):
            self.embed.set_footer(
                text = self.message.recommendationByPrice(language="en")[2]
            )

        return self.embed