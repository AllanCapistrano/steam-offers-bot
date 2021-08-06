from random import randint

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
        (
            gameFinalPrices[index] != "Gratuito para jogar" or 
            gameFinalPrices[index] != "Não disponível!"
        ) and
        maxPrice != None
    ):
        while(True):
            temp = gameFinalPrices[index]

            if(
                temp == "Gratuito para jogar" or 
                temp == "Não disponível!"
            ):
                break

            temp1      = temp.split("R$")[1]
            finalPrice = float(temp1.replace(",", "."))
            
            if(finalPrice < maxPrice):
                break
            
            index = randint(0, len(gameFinalPrices) - 1)

        return index

    return index