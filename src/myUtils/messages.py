def noOffers():
    msgList = []

    msgList.append(
        "😟 **Nenhum destaque encontrado no momento, tente novamente mais tarde!**")
    msgList.append(
        "😟 **Nenhuma promoção encontrada no momento, tente novamente mais tarde!**")

    return msgList


def checkDm():
    return "** Cheque sua DM** 😃"


def title():
    titleList = []

    titleList.append("Aqui está o link para o convite:")
    titleList.append("🎮 Jogo/Evento em Destaque 🎮")
    titleList.append("🕹️ Oferta do Dia 🕹️")
    titleList.append("📊 Informações 📊")

    return titleList


def priceAlert():
    return "⚠️Atenção, os preços estão em Dólar"