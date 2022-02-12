from typing import Literal

from discord import Embed

from services.messages import Message

class EmbedGameReview():
    def __init__(
        self,
        color: Literal, 
        gameName: str,
        gameImg: str,
        searchUrl: str,
        sumary: list,
        totalAmount: list,
        message: Message,
    ) -> None:
        """ Método construtor.

        Parameters
        -----------
        color: :class:`Literal`
        gameName: :class:`str`
        gameImg: :class:`str`
        searchUrl: :class:`str`
        sumary: :class:`list`
        totalAmount: :class:`list`
        message: :class:`Message`
        """
        
        self.color       = color
        self.gameName    = gameName
        self.gameImg     = gameImg
        self.searchUrl   = searchUrl
        self.sumary      = sumary
        self.totalAmount = totalAmount
        self.message     = message
        self.embed       = Embed(color=self.color)

    def embedGameReviewPortuguese(self):
        """ Monta a Embed do comando de análise em Português.

        Returns
        -----------
        embed: :class:`Embed`
        """

        if(len(self.sumary) > 0):
            if (self.sumary[0].find("positivas") != -1):
                self.embed.title = "👍 Análise: {} 👍".format(self.gameName)
            elif(self.sumary[0].find("negativas") != -1):
                self.embed.title = "👎 Análise: {} 👎".format(self.gameName)
            else:
                self.embed.title = "👍 Análise: {} 👎".format(self.gameName)
            
            self.embed.set_image(url=self.gameImg)

            if(len(self.sumary) == 1 and len(self.totalAmount) == 1):
                self.embed.add_field(
                    name   = "**Todas as análises:**", 
                    value  = "{} (Qtd. de análises: {})".format(self.sumary[0], self.totalAmount[0]), 
                    inline = False
                ) 
            elif(len(self.sumary) == 2 and len(self.totalAmount) == 2):
                self.embed.add_field(
                    name   = "**Análises Recentes:**", 
                    value  = "{} (Qtd. de análises: {})".format(self.sumary[0], self.totalAmount[0]), 
                    inline = False
                )
                self.embed.add_field(
                    name   = "**Todas as análises:**", 
                    value  = "{} (Qtd. de análises: {})".format(self.sumary[1], self.totalAmount[1]), 
                    inline = False
                )

            if(self.searchUrl != None):
                self.embed.add_field(
                    name   = "**Obs:**", 
                    value  = self.message.wrongGame(self.searchUrl), 
                    inline = False
                )
        else:
            self.embed.title = "⚠ Análise: {} ⚠".format(self.gameName)

            self.embed.set_image(url=self.gameImg)
            self.embed.add_field(
                name   = "**Observação:**", 
                value  = self.message.noReviews()[0], 
                inline = False
            )

        return self.embed

    def embedGameReviewEnglish(self):
        """ Monta a Embed do comando de análise em Inglês.

        Returns
        -----------
        embed: :class:`Embed`
        """

        if(len(self.sumary) > 0):
            if (self.sumary[0].find("positivas") != -1):
                self.embed.title = "👍 Review: {} 👍".format(self.gameName)
            elif(self.sumary[0].find("negativas") != -1):
                self.embed.title = "👎 Review: {} 👎".format(self.gameName)
            else:
                self.embed.title = "👍 Review: {} 👎".format(self.gameName)
            
            self.embed.set_image(url=self.gameImg)

            if(len(self.sumary) == 1 and len(self.totalAmount) == 1):
                self.embed.add_field(
                    name   = "**All reviews:**", 
                    value  = "{} (Number of reviews: {})".format(self.sumary[0], self.totalAmount[0]), 
                    inline = False
                ) 
            elif(len(self.sumary) == 2 and len(self.totalAmount) == 2):
                self.embed.add_field(
                    name   = "**Recent reviews:**", 
                    value  = "{} (Number of reviews: {})".format(self.sumary[0], self.totalAmount[0]), 
                    inline = False
                )
                self.embed.add_field(
                    name   = "**All reviews:**", 
                    value  = "{} (Number of reviews: {})".format(self.sumary[1], self.totalAmount[1]), 
                    inline = False
                )

            if(self.searchUrl != None):
                self.embed.add_field(
                    name   = "**PS:**", 
                    value  = self.message.wrongGame(
                        url      = self.searchUrl, 
                        language = "en"
                    ), 
                    inline = False
                )
        else:
            self.embed.title = "⚠ Review: {} ⚠".format(self.gameName)

            self.embed.set_image(url=self.gameImg)
            self.embed.add_field(
                name   = "**PS:**", 
                value  = self.message.noReviews(language="en")[0], 
                inline = False
            )

        return self.embed