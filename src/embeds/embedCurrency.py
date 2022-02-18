from typing import Literal

from discord import Embed

from services.messages import Message

class EmbedCurrency():
    def __init__(
        self,
        color: Literal, 
        message: Message,
    ) -> None:
        """ Método construtor.

        Parameters
        -----------
        color: :class:`Literal`
        message: :class:`Message`
        """
        
        self.color   = color
        self.message = message
        self.embed   = Embed(color=self.color)

    def embedCurrencyPortuguese(self, end: int, start: int = 0):
        """ Monta a Embed do comando de outras moedas em Português.

        Parameters
        -----------
        start: :class:`int`
            Índice inicial da lista das moedas.
        end: :class:`int`
            Índice final da lista das moedas.

        Returns
        -----------
        embed: :class:`Embed`
        """

        namesEmbed  = self.message.currenciesValues()
        valuesEmbed = self.message.helpCurrencies()

        if(len(namesEmbed) == len(valuesEmbed)):
            self.embed.title = self.message.title()[8]

            for index in range(start, end):
                self.embed.add_field(
                    name   = namesEmbed[index],
                    value  = valuesEmbed[index], 
                    inline = True
                )

            self.embed.add_field(
                name   = "Comandos que podem ser utilizados:",
                value  = "`$promoção`, `$categoria`, `$jogo`, `$gênero`, `$preçomáximo`",
                inline = False
            )

            self.embed.set_footer(text="Para utilizar: $[comando] | [moeda]. Ex: $promoção | cad")
            
            return self.embed

    def embedCurrencyEnglish(self, end: int, start: int = 0):
        """ Monta a Embed do comando de outras moedas em Inglês.

        Parameters
        -----------
        start: :class:`int`
            Índice inicial da lista das moedas.
        end: :class:`int`
            Índice final da lista das moedas.

        Returns
        -----------
        embed: :class:`Embed`
        """


        namesEmbed  = self.message.currenciesValues()
        valuesEmbed = self.message.helpCurrencies(language="en")
        
        if(len(namesEmbed) == len(valuesEmbed)):
            self.embed.title = self.message.title(language="en")[8]

            for index in range(start, end):
                self.embed.add_field(
                    name   = namesEmbed[index],
                    value  = valuesEmbed[index], 
                    inline = True
                )

            self.embed.add_field(
                name   = "Commands that can be used:",
                value  = "`$dailydeal`, `$gametab`, `$game`, `$genre`, `$maxprice`",
                inline = False
            )

            self.embed.set_footer(text="Try: $[command] | [currency]. Ex: $dailydeal | cad")
            
            return self.embed