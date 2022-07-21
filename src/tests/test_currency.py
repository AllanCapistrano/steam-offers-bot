from sys import path
path.append("../") # Habilita a importação dos arquivo que etão em src/*

import unittest
from services.currency import Currency

class TestCurrency(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.currency = Currency()

    def test_defineCurrency(self):
        """ Verifica se ao passar uma sequência de comandos com e sem a 
        especificação das moedas, se o método defineCurrency funciona 
        corretamente.
        
        """

        values = [
            ("pr"),
            ("pr", "|", "usd"),
            "pr",
            "pr | usd"
        ]

        excepted = [
            "br",
            "us"
        ]

        self.assertEqual(self.currency.defineCurrency(values[0]), excepted[0], "Deve ser 'br'")
        self.assertEqual(self.currency.defineCurrency(values[1]), excepted[1], "Deve ser 'us'")
        self.assertEqual(self.currency.defineCurrency(values[2]), excepted[0], "Deve ser 'br'")
        self.assertEqual(self.currency.defineCurrency(values[3]), excepted[1], "Deve ser 'us'")

    def test_formatCurrency(self):
        """Verifica se o método de formatação das moedas está funcionando
        corretamente.

        """

        value             = "CAD"
        expected          = "ca"
        currencyFormatted = self.currency.formatCurrency(value)

        self.assertEqual(currencyFormatted, expected, "Deve ser 'ca'")

    def test_formatCurrency_default_currency(self):
        """ Verifica se quando passar uma moeda inválida, retorna a moeda 
        padrão.

        """

        value             = "XYZ"
        expected          = "us"
        currencyFormatted = self.currency.formatCurrency(value)

        self.assertEqual(currencyFormatted, expected, "Deve ser 'us'")

    def test_currencyExists_True(self):
        """ Verifica se a moeda passada existe.

        """

        firstValue  = "CAD"
        secondValue = "XYZ"

        self.assertTrue(self.currency.currencyExists(firstValue), "Deve ser True")
        self.assertFalse(self.currency.currencyExists(secondValue), "Deve ser False")
    
if __name__ == "__main__":
    unittest.main()