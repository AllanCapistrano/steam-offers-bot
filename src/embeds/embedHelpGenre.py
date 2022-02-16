from typing import Literal

from discord import Embed

from services.messages import Message

class EmbedHelpGenre():
    def __init__(
        self,
        prefix: str, 
        color: Literal, 
        message: Message,
        imgGenres: list
    ) -> None:
        """ Método construtor.

        Parameters
        -----------
        prefix: :class:`str`
        color: :class:`Literal`
        message: :class:`Message`
        imgGenres: :class:`list`
        """

        self.prefix    = prefix
        self.color     = color
        self.message   = message
        self.imgGenres = imgGenres
        self.embed     = Embed(color=self.color)

    def embedHelpGenrePortuguese(self) -> Embed:
        """ Monta a Embed do comando de ajuda dos gêneros em Português.

        Returns
        -----------
        embed: :class:`Embed`
        """

        self.embed.title       = self.message.title()[4]
        self.embed.description = self.message.gameGenres()

        self.embed.add_field(
            name   = "Ficou confuso(a)?",
            value  = self.message.helpValues(img=self.imgGenres[0])[0],
            inline = False
        )
        self.embed.set_footer(text="Utilize {}gênero [um dos gêneros acima]".format(self.prefix))

        return self.embed

    def embedHelpGenreEnglish(self) -> Embed:
        """ Monta a Embed do comando de ajuda dos gêneros em Inglês.

        Returns
        -----------
        embed: :class:`Embed`
        """

        self.embed.title       = self.message.title(language="en")[4]
        self.embed.description = self.message.gameGenres(language="en")

        self.embed.add_field(
            name   = "Didn't understand?",
            value  = self.message.helpValues(language="en", img=self.imgGenres[1])[0],
            inline = False
        )
        self.embed.set_footer(text="Send {}genre [one of genres above]".format(self.prefix))

        return self.embed