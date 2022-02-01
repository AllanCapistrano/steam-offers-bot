from typing import Literal

from discord import Embed
from discord.ext.commands import Bot

from services.messages import Message

class EmbedHelp():
    def __init__(
        self,
        client: Bot, 
        prefix: str, 
        color: Literal, 
        urlInvite: str,
        reactions: list,
        message: Message
    ) -> None:
        """ Método construtor.

        Parameters
        -----------
        client: :class:`Bot`
        prefix: :class:`str`
        color: :class:`Literal`
        urlInvite: :class:`str`
        reactions: :class:`list`
        message: :class:`Message`
        """

        self.client    = client
        self.prefix    = prefix
        self.color     = color
        self.urlInvite = urlInvite
        self.ownerId   = 259443927441080330
        self.reactions = reactions
        self.message   = message
        self.embed     = Embed(color = self.color)

    def embedHelpPortuguese(self):
        """ Monta a Embed do comando de ajuda em português.
        """

        self.embed.set_author(
            name     = f"{self.client.user.name} lista de comandos:", 
            icon_url = self.client.user.avatar_url
        )
        self.embed.add_field(
            name   = "```{0}promoção``` ou ```{0}pr```".format(self.prefix),
            value  = self.message.helpValues()[1], 
            inline = False
        )
        self.embed.add_field(
            name   = "```{0}destaque``` ou ```{0}dt```".format(self.prefix),
            value  = self.message.helpValues()[2], 
            inline = False
        )
        self.embed.add_field(
            name   = "```{0}gametab [categoria]```".format(self.prefix),
            value  = self.message.helpValues(prefix=self.prefix)[13], 
            inline = False
        )
        self.embed.add_field(
            name   = "```{}convite```".format(self.prefix),
            value  = self.message.helpValues()[7], 
            inline = False
        )
        self.embed.add_field(
            name   = "```{}botinfo```".format(self.prefix),
            value  = self.message.helpValues()[8], 
            inline = False
        )
        self.embed.add_field(
            name   = "```{}game [nome do jogo]```".format(self.prefix),
            value  = self.message.helpValues()[9], 
            inline = False
        )
        self.embed.add_field(
            name   = "```{}genre [gênero do jogo]```".format(self.prefix),
            value  = self.message.helpValues()[10], 
            inline = False
        )
        self.embed.add_field(
            name   = "```{}maxprice [preço]```".format(self.prefix),
            value  = self.message.helpValues()[11], 
            inline = False
        )
        self.embed.add_field(
            name   = "```{0}análises [nome do jogo]``` ou ```{0}reviews [nome do jogo]```".format(self.prefix),
            value  = self.message.helpValues()[12], 
            inline = False
        )

        return self.embed

    def embedHelpEnglish(self):
        """ Monta a Embed do comando de ajuda em inglês.
        """

        self.embed.set_author(
            name     = f"{self.client.user.name} command list:", 
            icon_url = self.client.user.avatar_url
        )
        self.embed.add_field(
            name   = "```{0}dailyDeal``` or ```{0}dd```".format(self.prefix),
            value  = self.message.helpValues(language="en")[1], 
            inline = False
        )
        self.embed.add_field(
            name   = "```{0}spotlight``` or ```{0}sl```".format(self.prefix),
            value  = self.message.helpValues(language="en")[2], 
            inline = False
        )
        self.embed.add_field(
            name   = "```{0}gametab [category]```".format(self.prefix),
            value  = self.message.helpValues(
                language = "en", 
                prefix   = self.prefix
            )[13], 
            inline = False
        )
        self.embed.add_field(
            name   = "```{}invite```".format(self.prefix),
            value  = self.message.helpValues(language="en")[7], 
            inline = False
        )
        self.embed.add_field(
            name   = "```{}botinfo```".format(self.prefix),
            value  = self.message.helpValues(language="en")[8], 
            inline = False
        )
        self.embed.add_field(
            name   = "```{}game [game name]```".format(self.prefix),
            value  = self.message.helpValues(language="en")[9], 
            inline = False
        )
        self.embed.add_field(
            name   = "```{}genre [game genre]```".format(self.prefix),
            value  = self.message.helpValues(language="en")[10], 
            inline = False
        )
        self.embed.add_field(
            name   = "```{}maxprice [price]```".format(self.prefix),
            value  = self.message.helpValues(language="en")[11], 
            inline = False
        )
        self.embed.add_field(
            name   = "```{0}review [game name]```".format(self.prefix),
            value  = self.message.helpValues(language="en")[12], 
            inline = False
        )

        return self.embed