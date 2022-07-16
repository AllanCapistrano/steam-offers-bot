class Currency:
    def __init__(self):
        """ Método construtor.

        """

        self.currencies      = [
        "AED",
        "ARS",
        "AUD",
        "BRL",
        "CAD",
        "CHF",
        "CLP",
        "CNY",
        "COP",
        "CRC",
        "EUR",
        "GBP",
        "HKD",
        "ILS",
        "IDR",
        "INR",
        "JPY",
        "KRW",
        "KWD",
        "KZT",
        "MXN",
        "MYR",
        "NOK",
        "NZD",
        "PEN",
        "PHP",
        "PLN",
        "QAR",
        "RUB",
        "SAR",
        "SGD",
        "THB",
        "TRY",
        "TWD",
        "UAH",
        "USD",
        "UYU",
        "VND",
        "ZAR"
    ]
        self.defaultCurrency = "BRL"

    def defineCurrency(self, args: tuple | str, defaultCurrency: str = "br") -> str:
        """ Define a moeda do comando utilizado.

        Parameters
        -----------
        args: :class:`tuple` | :class: `str`
            Lista de argumentos do comando.
        defaultCurrency: :class:`str`
            Moeda padrão do comando

        Returns
        -----------
        currency: :class:`str`
        """

        if(type(args) is tuple):
            if(len(args) > 0):
                index = 0

                for commandArg in args:
                    if(commandArg == "|"):
                        try:
                            return self.formatCurrency(args[index + 1])
                        except:
                            return defaultCurrency
                        
                    index += 1

        elif(type(args) is str):
            if(args.find(" | ") != -1):
                command = args.split(" | ")

                return self.formatCurrency(command[1])

        return defaultCurrency

    def currencyExists(self, c: str) -> bool:
        """ Verifica se a moeda passada esta disponível na Steam.

        Parameters
        -----------
        c: :class:`str`
            Moeda digitada.

        Returns
        -----------
        Boolean: :class:`bool`
        """
        
        for currency in self.currencies:
            if(c.upper() == currency):
                return True
        
        return False

    def formatCurrency(self, currency: str) -> str:
        """ Formata a moeda passada para o formato que a Steam aceita. Caso a 
        moeda passada não seja válida, a moeda padrão é o dólar (USD).

        Parameters
        -----------
        currency: :class:`str`
            Moeda digitada.

        Returns
        -----------
        formattedCurrency: :class:`str`
        """
        
        if(self.currencyExists(currency)):
            return currency[0:2].lower()
        
        return "us"