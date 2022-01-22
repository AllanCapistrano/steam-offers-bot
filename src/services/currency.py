class Currency:
    currencies      = [
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
    defaultCurrency = "BRL"
    
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
            if(c == currency):
                return True
        return False