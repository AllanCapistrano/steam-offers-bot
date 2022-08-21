from typing import Literal

from discord import Embed
from discord.ext.commands import Bot

from services.messages import Message

class EmbedInvite():
    def __init__(
        self,
        client: Bot,
        color: Literal, 
        message: Message,
        urlInvite: str
    ) -> None:
        """ Método construtor.

        Parameters
        -----------
        client: :class:`Bot`
        color: :class:`Literal`
        message: :class:`Message`
        urlInvite: :class:`str`
        """

        self.client    = client
        self.color     = color
        self.message   = message
        self.urlInvite = urlInvite
        self.embed     = Embed(
            color       = self.color,
            description = f"**{self.urlInvite}**",
        )

    def embedInvitePortuguese(self):
        """ Monta a Embed do comando de convite em Português.

        Returns
        -----------
        embed: :class:`Embed`
        """
        
        self.embed.title = self.message.title()[0]
        self.embed.set_thumbnail(url=self.client.user.avatar)

        return self.embed

    def embedInviteEnglish(self):
        """ Monta a Embed do comando de convite em Inglês.

        Returns
        -----------
        embed: :class:`Embed`
        """
        
        self.embed.title = self.message.title(language="english")[0]
        self.embed.set_thumbnail(url=self.client.user.avatar)

        return self.embed