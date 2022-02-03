from typing import Literal

from discord import Embed

from services.messages import Message

class EmbedGenre():
    def __init__(
        self,
        color: Literal, 
        gameGenreToSearch: str,
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
        gameName: :class:`gameName`
        gameImg: :class:`gameImg`
        gameUrl: :class:`gameUrl`
        gameOriginalPrice: :class:`gameOriginalPrice`
        gameFinalPrice: :class:`gameFinalPrice`
        message: :class:`Message`
        """
        
        self.color             = color
        self.gameGenreToSearch = gameGenreToSearch
        self.gameImg           = gameImg
        self.gameUrl           = gameUrl
        self.gameOriginalPrice = gameOriginalPrice
        self.gameFinalPrice    = gameFinalPrice
        self.message           = message
        self.embed             = Embed(color=self.color)

    def embedGenrePortuguese(self):
        """ Monta a Embed do comando de gênero em Português.

        Returns
        -----------
        embed: :class:`Embed`
        """
        
        self.embed.title = self.message.title(genre=self.gameGenreToSearch)[6]

        self.embed.set_image(url=self.gameImg)
        self.embed.add_field(
            name   = "**Nome:**", 
            value  = "**{}**".format(self.gameName), 
            inline = False
        )
        self.embed.add_field(
            name   = "**Link:**", 
            value  = "**[Clique Aqui]({})**".format(self.gameUrl), 
            inline = False
        )

        if(
            (self.gameOriginalPrice == self.gameFinalPrice) and 
            (self.gameOriginalPrice != "Gratuito p/ Jogar")
        ):
            self.embed.add_field(
                name   = "**Preço:**", 
                value  = "**{}**".format(self.gameOriginalPrice), 
                inline = True
            )
        else:
            if(self.gameOriginalPrice != "Gratuito p/ Jogar"):
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
            else:
                self.embed.add_field(
                    name   = "**Preço:**", 
                    value  = "**{}**".format(self.gameOriginalPrice), 
                    inline = True
                )

    def embedGenreEnglish(self):
        """ Monta a Embed do comando de gênero em Inglês.

        Returns
        -----------
        embed: :class:`Embed`
        """

        self.embed.title = self.message.title(
            language="en",
            genre=self.gameGenreToSearch
        )[6]

        self.embed.set_image(url=self.gameImg)
        self.embed.add_field(
            name   = "**Game Name:**", 
            value  = "**{}**".format(self.gameName), 
            inline = False
        )
        self.embed.add_field(
            name   = "**Link:**", 
            value  = "**[Click Here]({})**".format(self.gameUrl), 
            inline = False
        )

        if(
            (self.gameOriginalPrice == self.gameFinalPrice) and 
            (self.gameOriginalPrice != "Free to Play")
        ):
            self.embed.add_field(
                name   = "**Price:**", 
                value  = "**{}**".format(self.gameOriginalPrice), 
                inline = True
            )
        else:
            if(self.gameOriginalPrice != "Free to Play"):
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
            else:
                self.embed.add_field(
                    name   = "**Price:**", 
                    value  = "**{}**".format(self.gameOriginalPrice), 
                    inline = True
                )