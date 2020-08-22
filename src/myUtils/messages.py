# Mensagens para quando não existem promoções ou jogos em destaque.
def noOffers():
    msgList = []

    msgList.append(
        "😟 **Nenhum destaque encontrado no momento, tente novamente mais tarde!**")
    msgList.append(
        "😟 **Nenhuma promoção encontrada no momento, tente novamente mais tarde!**")

    return msgList

# Mensagem para as promoções que são enviadas para o privado.
def checkDm():
    return "** Cheque sua DM** 😃"

# Títulos das embeds.
def title():
    titleList = []

    titleList.append("Aqui está o link para o convite:")
    titleList.append("🎮 Jogo/Evento em Destaque 🎮")
    titleList.append("🕹️ Oferta do Dia 🕹️")
    titleList.append("📊 Informações 📊")

    return titleList

# Alerta dos valores exibidos.
def currencyAlert():
    return "⚠️Atenção, os preços estão em Dólar"