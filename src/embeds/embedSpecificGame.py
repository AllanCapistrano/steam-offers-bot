from typing import Literal

from discord import Embed

from services.messages import Message

class EmbedSpecificGame():
    def __init__(
        self,
        color: Literal, 
        gameName: str,
        gameImg: str,
        gameUrl: str,
        gameOriginalPrice: str,
        gameFinalPrice: str,
        gameDescription: str,
        searchUrl: str,
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
        gameDescription: :class:`str`
        searchUrl: :class:`str`
        message: :class:`Message`
        """
        
        self.color             = color
        self.gameName          = gameName
        self.gameImg           = gameImg
        self.gameUrl           = gameUrl
        self.gameOriginalPrice = gameOriginalPrice
        self.gameFinalPrice    = gameFinalPrice
        self.gameDescription   = gameDescription
        self.searchUrl         = searchUrl
        self.message           = message
        self.embed             = Embed(color=self.color)

    def embedSpecificGamePortuguese(self) -> Embed:
        """ Monta a Embed do comando de jogo específico em Português.

        Returns
        -----------
        embed: :class:`Embed`
        """

        self.embed.title = self.message.title(gameName=self.gameName)[5]

        self.embed.set_image(url=self.gameImg)
        self.embed.add_field(
            name   = "**Link:**", 
            value  = "**[Clique Aqui]({})**".format(self.gameUrl), 
            inline = False
        )

        if(self.gameOriginalPrice != self.gameFinalPrice): # Caso o jogo esteja em promoção.
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

        if(self.gameDescription != None):
            self.embed.add_field(
                name   = "**Descrição:**", 
                value  = "{}".format(self.gameDescription), 
                inline = False
            )

        if(self.searchUrl != None): # Caso seja passado o nome do jogo.
            self.embed.add_field(
                name   = "**Obs:**", 
                value  = self.message.wrongGame(self.searchUrl), 
                inline = False
            )
        
        return self.embed

    def embedSpecificGameEnglish(self) -> Embed:
        """ Monta a Embed do comando de jogo específico em Inglês.

        Returns
        -----------
        embed: :class:`Embed`
        """

        self.embed.title = self.message.title(
            gameName = self.gameName,
            language = "en"
        )[5]

        self.embed.set_image(url=self.gameImg)
        self.embed.add_field(
            name   = "**Link:**", 
            value  = "**[Clique Here]({})**".format(self.gameUrl), 
            inline = False
        )

        if(self.gameOriginalPrice != self.gameFinalPrice): # Caso o jogo esteja em promoção.
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

        if(self.gameDescription != None):
            self.embed.add_field(
                name   = "**Description:**", 
                value  = "{}".format(self.gameDescription), 
                inline = False
            )

        if(self.searchUrl != None): # Caso seja passado o nome do jogo.
            self.embed.add_field(
                name   = "**PS:**", 
                value  = self.message.wrongGame(
                    url      = self.searchUrl,
                    language = "en"
                ), 
                inline = False
            )
        
        return self.embed