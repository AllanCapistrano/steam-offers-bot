from random import randint

# Randomiza uma mensagem de uma lista de mensagens.
def randomMessage(msg, size):
    msgR = msg[randint(0, size - 1)]

    return msgR

# Mensagens para quando não existem promoções ou jogos em destaque.
def noOffers():
    msgList = []

    # Mensagem de destaque.
    msgList.append(
        "😟 **Nenhum destaque encontrado no momento, tente novamente mais tarde!**")
    # Mensagem de promção.
    msgList.append(
        "😟 **Nenhuma promoção encontrada no momento, tente novamente mais tarde!**")
    # Mensagem de jogo específico.
    msgList.append(
        "😟 **Jogo não encontrado! Por favor verifique o nome digitado.**"
    )
    # Mensagem de gênero do jogo.
    msgList.append(
        "😟 **Gênero não encontrado! Por favor verifique o que foi digitado ou " + \
        "utilize `$help genre` para verificar a lista completa dos gêneros dos jogos.**"
    )

    return msgList

# Mensagem para as promoções que são enviadas para o privado.
def checkDm():
    return "** Cheque sua DM** 😃"

# Títulos das embeds.
def title(genre = None):
    titleList = []

    titleList.append("Aqui está o link para o convite:")
    titleList.append("🎮 Jogo/Evento em Destaque 🎮")
    titleList.append("🕹️ Oferta do Dia 🕹️")
    titleList.append("📊 Informações 📊")
    titleList.append("🎮 Gêneros dos Jogos 🕹️")
    
    if(genre == "casual" or genre == "indie" or genre == "multijogador massivo" or genre == "rpg"):
        titleList.append("🎮 Jogo {} recomendado 🕹️".format(genre))
    else:
        titleList.append("🎮 Jogo de {} recomendado 🕹️".format(genre))

    return titleList

# Alerta dos valores exibidos.
def currencyAlert():
    return "⚠️Atenção, os preços estão em Dólar."

# Conteúdo do comando $help.
def helpValues():
    msgList = []

    msgList.append(
        "**Exibe quais jogos estão na promoção diária da Steam ou gratuitos por um tempo limitado.**")
    msgList.append(
        "**Exibe os eventos que estão em destaque na Steam, ou os jogos em promoção que estão em destaque na loja.**")
    msgList.append(
        "**Exibe quais jogos da categoria \"Novidades Populares\" estão em promoção na loja.**")
    msgList.append(
        "**Exibe quais jogos da categoria \"Mais Vendidos\" estão em promoção na loja.**")
    msgList.append(
        "**Exibe quais jogos da categoria \"Mais Jogados\" estão em promoção na loja.**")
    msgList.append(
        "**Exibe quais jogos da categoria \"Pré-compra\" estão em promoção na loja.**")
    msgList.append(
        "**Gera o convite para que o Bot possa ser adicionado em outros servidores.**")
    msgList.append("**Exibe as informações do Bot.**")
    msgList.append("**Busca um jogo pelo nome e exibe as suas informações. Obs: Não precisa dos [].**")
    msgList.append("**Recomenda um jogo a partir do gênero especificado. Obs: Não precisa dos [].**")

    return msgList

# Conteúdo do comando $botinfo.
def infoValues():
    msgList = []

    msgList.append("**3.9.0**") # Versão Python
    msgList.append("**1.5.1**") # Versão Discord.py
    msgList.append("**Bot feito para notificar os jogos que estão em promoção, " 
        "sem a necessidade de abrir a loja da Steam ou sair do Discord. "
        "Criado por ArticZ#1081**") # Informações.
    msgList.append("02 de Janeiro de 2021") # Data da última atualização.

    return msgList

# Mensagens de status do Bot.
def status(numServers):
    statusList = []

    statusList.append("$help | {} Servidores".format(numServers))
    statusList.append("$destaque | {} Servidores".format(numServers))
    statusList.append("$promocao | {} Servidores".format(numServers))
    statusList.append("$botinfo | {} Servidores".format(numServers))
    statusList.append("$convite | {} Servidores".format(numServers))
    statusList.append("$game [nome] | {} Servidores".format(numServers))
    statusList.append("$genre [gênero] | {} Servidores".format(numServers))

    return statusList

# Mensagens de erros durante o envio do comando.
def commandAlert():
    alertList = []

    alertList.append("⚠️ **Informe o nome do jogo! Ex: `$game undertale`**")
    alertList.append("⚠️ **Informe o gênero do jogo! Ex: `$genre casual`**")
    alertList.append("⚠️ **Comando inválido!**")

    return alertList

# Mensagem de busca pelo jogo errado.
def wrongGame(url):
    return "Não era o jogo que estava buscando? [Clique Aqui]({}) para visualizar a lista completa dos jogos.".format(url)

# Gêneros dos jogos.
def gameGenres():
    genreList = []

    genreList.append("**Aventura**")
    genreList.append("**Ação**")
    genreList.append("**Casual**")
    genreList.append("**Corrida**")
    genreList.append("**Esportes**")
    genreList.append("**Estratégia**")
    genreList.append("**Indie**")
    genreList.append("**Multijogador Massivo**")
    genreList.append("**RPG**")
    genreList.append("**Simulação**")

    return genreList

# Emojis dos gêneros dos jogos.
def emojisGameGenres():
    emojisList = []
    
    emojisList.append("🤠")
    emojisList.append("🔫")
    emojisList.append("💻")
    emojisList.append("🏎️")
    emojisList.append("🏆")
    emojisList.append("🧠")
    emojisList.append("🕹️")
    emojisList.append("🌐")
    emojisList.append("🧙")
    emojisList.append("🖱️")

    return emojisList