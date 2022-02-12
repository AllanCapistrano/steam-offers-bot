from typing import Literal

from discord import Embed

from services.messages import Message

class EmbedDailyGame():
    def __init__(
        self,
        color: Literal, 
        gameImg: str,
        gameUrl: str,
        gameOriginalPrice: str,
        gameFinalPrice: str,
        message: Message,
    ) -> None:
        """ Método construtor.

        Parameters
        -----------
        color: :class:`Literal`
        gameImg: :class:`str`
        gameUrl: :class:`str`
        gameOriginalPrice: :class:`str`
        gameFinalPrice: :class:`str`
        message: :class:`Message`
        """
        
        self.color             = color
        self.gameImg           = gameImg
        self.gameUrl           = gameUrl
        self.gameOriginalPrice = gameOriginalPrice
        self.gameFinalPrice    = gameFinalPrice
        self.message           = message
        self.embed             = Embed(color=self.color)

    def embedDailyGamePortuguese(self) -> Embed:
        """ Monta a Embed do comando de jogos em promoção diária em Português.

        Returns
        -----------
        embed: :class:`Embed`
        """

        self.embed.title = self.message.title()[2]

        self.embed.set_image(url=self.gameImg)
        self.embed.add_field(
            name   = "**Link:**", 
            value  = f"**[Clique Aqui]({self.gameUrl})**", 
            inline = False
        )

        if(self.gameOriginalPrice == self.gameFinalPrice):
            self.embed.add_field(
                name   = "**Preço:**", 
                value  = f"**{self.gameOriginalPrice}**", 
                inline = True
            )
        else:
            self.embed.add_field(
                name   = "**Preço Original:**", 
                value  = f"**{self.gameOriginalPrice}**", 
                inline = True
            )
            self.embed.add_field(
                name   = "**Preço com Desconto:**", 
                value  = f"**{self.gameFinalPrice}**", 
                inline = True
            )

        return self.embed
    
    def embedDailyGameEnglish(self) -> Embed:
        """ Monta a Embed do comando de jogos em promoção diária em inglês.

        Returns
        -----------
        embed: :class:`Embed`
        """

        self.embed.title = self.message.title(language="en")[2]

        self.embed.set_image(url=self.gameImg)
        self.embed.add_field(
            name   = "**Link:**", 
            value  = f"**[Click Here]({self.gameUrl})**", 
            inline = False
        )

        if(self.gameOriginalPrice == self.gameFinalPrice):
            self.embed.add_field(
                name   = "**Price:**", 
                value  = f"**{self.gameOriginalPrice}**", 
                inline = True
            )
        else:
            self.embed.add_field(
                name   = "**Original Price:**", 
                value  = f"**{self.gameOriginalPrice}**", 
                inline = True
            )
            self.embed.add_field(
                name   = "**Discount Price:**", 
                value  = f"**{self.gameFinalPrice}**", 
                inline = True
            )

        return self.embed