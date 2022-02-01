from typing import Literal

from discord import Embed
from discord.ext.commands import Bot

from services.messages import Message

class EmbedHelpGameTab():
    def __init__(
        self,
        client: Bot,
        prefix: str, 
        color: Literal, 
        message: Message,
    ) -> None:
        """ Método construtor.

        Parameters
        -----------
        prefix: :class:`str`
        color: :class:`Literal`
        message: :class:`Message`
        imgGenres: :class:`list`
        """

        self.client  = client
        self.prefix  = prefix
        self.color   = color
        self.message = message
        self.embed   = Embed(color=self.color)

    def embedHelpGameTabPortuguese(self) -> Embed:
        """ Monta a Embed do comando de ajuda das categorias em Português.

        Returns
        -----------
        embed: :class:`Embed`
        """

        self.embed.set_author(
            name     = f"{self.client.user.name} comando {self.prefix}categoria:", 
            icon_url = self.client.user.avatar_url
        )
        self.embed.add_field(
            name   = "```{0}categoria novidades populares``` ou ```{0}categoria np```".format(self.prefix),
            value  = self.message.helpValues()[3], 
            inline = False
        )
        self.embed.add_field(
            name   = "```{0}categoria mais vendidos``` ou ```{0}categoria mv```".format(self.prefix),
            value  = self.message.helpValues()[4], 
            inline = False
        )
        self.embed.add_field(
            name   = "```{0}categoria jogos populares``` ou ```{0}categoria jp```".format(self.prefix),
            value  = self.message.helpValues()[5], 
            inline = False
        )
        self.embed.add_field(
            name   = "```{0}categoria pré-venda``` ou ```{0}categoria pv```".format(self.prefix),
            value  = self.message.helpValues()[6], 
            inline = False
        )

        return self.embed

    def embedHelpGameTabEnglish(self) -> Embed:
        """ Monta a Embed do comando de ajuda das categorias em Inglês.

        Returns
        -----------
        embed: :class:`Embed`
        """

        self.embed.add_field(
            name   = "```{0}gametab new tranding``` or ```{0}gametab nt```".format(self.prefix),
            value  = self.message.helpValues(language="en")[3], 
            inline = False
        )
        self.embed.add_field(
            name   = "```{0}gametab top sellers``` or ```{0}gametab tp```".format(self.prefix),
            value  = self.message.helpValues(language="en")[4], 
            inline = False
        )
        self.embed.add_field(
            name   = "```{0}gametab being played ``` or ```{0}gametab bp```".format(self.prefix),
            value  = self.message.helpValues(language="en")[5], 
            inline = False
        )
        self.embed.add_field(
            name   = "```{0}gametab pre-purchase``` or ```{0}gametab pp```".format(self.prefix),
            value  = self.message.helpValues(language="en")[6], 
            inline = False
        )

        return self.embed