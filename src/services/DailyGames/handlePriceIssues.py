def handlePriceIssues(originalPrices: list, finalPrices: list) -> tuple[list, list]:
    """ Função responsável por corrigir eventuais incoerências nos preços dos
    jogos que estão em promoção.

    Parameters
    -----------
    originalPrices: :class:`list`
        Lista contendo os preços originais dos jogos.
    finalPrices: :class:`list`
        Lista contendo os preços com desconto dos jogos

    Returns
    -----------
    originalPrices: :class:`list`
    finalPrices: :class:`list`
    """
    
    originalPricesSize = len(originalPrices)
    finalPricesSize    = len(finalPrices)

    if(originalPricesSize == finalPricesSize):
        for x in (0, originalPricesSize - 1):
            if(
                (
                    originalPrices[x] == "Não disponível!" and
                    finalPrices[x].find("Gratuito") != -1
                ) 
                or
                (
                    originalPrices[x].find("Gratuito") != -1 and
                    finalPrices[x] == "Não disponível!"
                )
            ):
                originalPrices[x] = "Não disponível!"
                finalPrices[x]    = "Não disponível!"

    return originalPrices, finalPrices