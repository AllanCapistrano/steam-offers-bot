from typing import Literal

from discord import Embed
from discord.ext.commands import Bot

from services.messages import Message

class EmbedBotInfo():
    def __init__(
        self,
        client: Bot,
        color: Literal, 
        message: Message,
        ownerId: int
    ) -> None:
        """ Método construtor.

        Parameters
        -----------
        client: :class:`Bot`
        color: :class:`Literal`
        message: :class:`Message`
        ownerId: :class:`int`
        """

        self.client  = client
        self.color   = color
        self.message = message
        self.ownerId = ownerId
        self.embed   = Embed(color=self.color)
    
    def embedBotInfoPortuguese(self) -> Embed:
        """ Monta a Embed do comando de informações do Bot em Português.

        Returns
        -----------
        embed: :class:`Embed`
        """

        self.embed.title = self.message.title()[3]

        self.embed.set_thumbnail(url=self.client.user.avatar_url)
        self.embed.add_field(
            name   = "Python", 
            value  = self.message.infoValues()[0], 
            inline = True
        )
        self.embed.add_field(
            name   = "discord.py", 
            value  = self.message.infoValues()[1], 
            inline = True
        )
        self.embed.add_field(
            name   = "Sobre {}".format(self.client.user.name), 
            value  = self.message.infoValues()[2] + 
            self.client.get_user(self.ownerId).name + "#" 
            + self.client.get_user(self.ownerId).discriminator + "**", 
            inline = False
        )
        self.embed.set_author(
            name     = self.client.get_user(self.ownerId).name + "#" 
            + self.client.get_user(self.ownerId).discriminator, 
            icon_url = self.client.get_user(self.ownerId).avatar_url
        )
        self.embed.set_footer(
            text="Criado em 26 de Maio de 2020! | Última atualização em {}."
            .format(self.message.infoValues()[3])
        )

        return self.embed

    def embedBotInfoEnglish(self) -> Embed:
        """ Monta a Embed do comando de informações do Bot em Inglês.

        Returns
        -----------
        embed: :class:`Embed`
        """

        self.embed.title = self.message.title(language="en")[3]

        self.embed.set_thumbnail(url=self.client.user.avatar_url)
        self.embed.add_field(
            name   = "Python", 
            value  = self.message.infoValues(language="en")[0], 
            inline = True
        )
        self.embed.add_field(
            name   = "discord.py", 
            value  = self.message.infoValues(language="en")[1], 
            inline = True
        )
        self.embed.add_field(
            name   = "About {}".format(self.client.user.name), 
            value  = self.message.infoValues(language="en")[2] + 
            self.client.get_user(self.ownerId).name + "#" 
            + self.client.get_user(self.ownerId).discriminator + "**", 
            inline = False
        )
        self.embed.set_author(
            name     = self.client.get_user(self.ownerId).name + "#" 
            + self.client.get_user(self.ownerId).discriminator, 
            icon_url = self.client.get_user(self.ownerId).avatar_url
        )
        self.embed.set_footer(
            text="Created May 26, 2020! | Last update on {}."
            .format(self.message.infoValues(language="en")[3])
        )

        return self.embed