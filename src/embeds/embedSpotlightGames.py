from typing import Literal

from discord import Embed

from services.messages import Message

class EmbedSpotlightGames():
    def __init__(
        self,
        color: Literal, 
        gameImg: str,
        gameUrl: str,
        gameContent: str,
        message: Message,
    ) -> None:
        """ Método construtor.

        Parameters
        -----------
        color: :class:`Literal`
        gameImg: :class:`str`
        gameUrl: :class:`str`
        gameContent: :class:`str`
        message: :class:`Message`
        """
        
        self.color       = color
        self.gameImg     = gameImg
        self.gameUrl     = gameUrl
        self.gameContent = gameContent
        self.message     = message
        self.embed       = Embed(color=self.color)

    def embedSpotlightGamesPortuguese(self) -> Embed:
        """ Monta a Embed do comando de jogos em destaque em Português.

        Returns
        -----------
        embed: :class:`Embed`
        """

        self.embed.title = self.message.title()[1]

        self.embed.set_image(url=self.gameImg)
        self.embed.add_field(
            name   = "**Link:**", 
            value  = "**[Clique Aqui]({})**".format(self.gameUrl), 
            inline = False
        )
        self.embed.add_field(
            name   = "**Descrição:**", 
            value  = "**{}**".format(self.gameContent), 
            inline = False
        )

        return self.embed

    def embedSpotlightGamesEnglish(self) -> Embed:
        """ Monta a Embed do comando de jogos em destaque em Inglês.

        Returns
        -----------
        embed: :class:`Embed`
        """

        self.embed.title = self.message.title(language="en")[1]

        self.embed.set_image(url=self.gameImg)
        self.embed.add_field(
            name   = "**Link:**", 
            value  = "**[Click Here]({})**".format(self.gameUrl), 
            inline = False
        )
        self.embed.add_field(
            name   = "**Description:**", 
            value  = "**{}**".format(self.gameContent), 
            inline = False
        )

        return self.embed