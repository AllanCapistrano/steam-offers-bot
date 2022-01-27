from random import randint

def priceToFloat(price: str) ->float:
    """Transforma o preço no formato String em um número de ponto flutuante.
    
    Parameters
    -----------
    price: :class:`str`
        Preço no formato String.

    Returns
    -----------
    price: :class:`float`
    """

    index = 0

    for x in range(len(price)):
        if(price[x].isnumeric()):
            index = x
            break

    return float(price[index:len(price)].replace(",", "."))

def verifyPriceRange(maxPrice: float, gameFinalPrices: list) -> int:
    """Função que verifica se o jogo está na faixa de preço indicada, e retorna
    a posição da lista de um jogo que satisfaz essa faixa.
    
    Parameters
    -----------
    maxPrice: :class:`float`
        Faixa de preço.
    gameFinalPrices: :class: `list`
        Lista dos preços dos jogos.

    Returns
    -----------
    index: :class:`int`
    """

    index = randint(0, len(gameFinalPrices) - 1)

    if(
        gameFinalPrices[index].find("Gratuito") == -1 and # Se for gratuito não precisa verificar o preço
        gameFinalPrices[index].find("Free")     == -1 and
        gameFinalPrices[index] != "Não disponível!"   and
        maxPrice != 0.0
    ):
        while(True):
            temp = gameFinalPrices[index]

            if(
                temp.find("Gratuito") != -1 or 
                temp.find("Free")     != -1 or 
                temp                  == "Não disponível!"
            ):
                break

            finalPrice = priceToFloat(temp)
            
            if(finalPrice < maxPrice):
                break
            
            index = randint(0, len(gameFinalPrices) - 1)

        return index

    return index