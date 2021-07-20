from random import randint

def randomMessage(msg: list) -> str:
    """ Função retornar uma mensagem aleatória.

    Parameters
    -----------
    msg: :class:`list`
        Lista de mensagens.

    Returns
    -----------
    message: :class:`str`
    """

    return msg[randint(0, len(msg) - 1)]

def noOffers() -> list:
    """ Mensagens para quando não existem promoções ou jogos em destaque.

    Returns
    -----------
    msgList: :class:`list`
    """

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
        "utilize o comando `$help genre` para verificar a lista completa dos " + \
        "gêneros disponíveis.**"
    )

    return msgList

def checkDm() -> list:
    """ Mensagem para as promoções que são enviadas para o privado.

    Returns
    -----------
    message: :class:`str`
    """
    
    return "** Cheque sua DM** 😃"

def title(genre: str = None , gameName: str = None) -> list:
    """ Títulos das embeds.

    Returns
    -----------
    titleList: :class:`list`
    """
    
    titleList = []

    titleList.append("Aqui está o link para o convite:")
    titleList.append("🎮 Jogo/Evento em Destaque 🎮")
    titleList.append("🕹️ Oferta do Dia 🕹️")
    titleList.append("📊 Informações 📊")
    titleList.append("🎮 Gêneros dos Jogos 🕹️")
    
    if(genre == "casual" or genre == "indie" or genre == "multijogador massivo" or genre == "rpg"):
        titleList.append("🎮 Jogo __{}__ recomendado 🕹️".format(genre))
    else:
        titleList.append("🎮 Jogo de __{}__ recomendado 🕹️".format(genre))

    titleList.append("💰 Jogo: {} 💰".format(gameName))

    return titleList

def helpValues() -> list:
    """ Conteúdo do comando $help.

    Returns
    -----------
    msgList: :class:`list`
    """
    
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
    msgList.append("**Recomenda um jogo dada uma faixa máxima de preço. Obs: Não precisa dos [].**")

    return msgList

def infoValues() -> list:
    """ Conteúdo do comando $botinfo.

    Returns
    -----------
    msgList: :class:`list`
    """
    
    msgList = []

    msgList.append("**3.9.5**") # Versão Python
    msgList.append("**1.7.2**") # Versão Discord.py
    msgList.append("**Bot feito para notificar os jogos que estão em promoção, " 
        "sem a necessidade de abrir a loja da Steam ou sair do Discord. "
        "Criado por ArticZ#1081**") # Informações.
    msgList.append("20 de Julho de 2021") # Data da última atualização.

    return msgList

def status(prefix: str, numServers: int) -> list:
    """ Mensagens de status do Bot.

    Returns
    -----------
    statusList: :class:`list`
    """
    
    statusList = []

    statusList.append("{}help | {} Servidores".format(prefix, numServers))
    statusList.append("{}destaque | {} Servidores".format(prefix, numServers))
    statusList.append("{}promocao | {} Servidores".format(prefix, numServers))
    statusList.append("{}botinfo | {} Servidores".format(prefix, numServers))
    statusList.append("{}convite | {} Servidores".format(prefix, numServers))
    statusList.append("{}game [nome] | {} Servidores".format(prefix, numServers))
    statusList.append("{}genre [gênero] | {} Servidores".format(prefix, numServers))
    statusList.append("{}maxprice [preço] | {} Servidores".format(prefix, numServers))

    return statusList

def commandAlert() -> list:
    """ Mensagens de erro durante o envio de um comando.

    Returns
    -----------
    alertList: :class:`list`
    """
    
    alertList = []

    alertList.append("⚠️ **Informe o nome do jogo! Ex: `$game undertale`**")
    alertList.append("⚠️ **Informe o gênero do jogo! Ex: `$genre casual`**")
    alertList.append("⚠️ **Comando inválido!**")

    return alertList

def wrongGame(url: str) -> str:
    """ Mensagem de erro ao buscar um jogo específico.

    Parameters
    -----------
    url: :class:`str`

    Returns
    -----------
    message: :class:`srt`
    """

    return "Não era o jogo que estava buscando? [Clique Aqui]({}) para visualizar a lista completa dos jogos.".format(url)

def gameGenres() -> list:
    """ Gêneros dos jogos.

    Returns
    -----------
    genreList: :class:`list`
    """
    
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

def emojisGameGenres() -> list:
    """ Emojis dos gêneros dos jogos.

    Returns
    -----------
    emojisList: :class:`list`
    """
    
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

def searchMessage() -> list:
    """ Mensagens de busca.

    Returns
    -----------
    msgList: :class:`list`
    """
    
    msgList = []

    msgList.append("**🔎 Procurando.**")
    msgList.append("**🔎 Procurando pelo jogo")
    msgList.append("**🔎 Procurando por um jogo do gênero")
    msgList.append("**🔎 Procurando por um jogo de até __R$")


    return msgList

def recommendationByPrice() -> list:
    """ Mensagens de recomendação de jogo por preço.

    Returns
    -----------
    msgList: :class:`list`
    """
    
    msgList = []

    msgList.append(
        "**Faixa de preço inválida! Tente novamente.**"
    )
    msgList.append(
        "A faixa máxima de preço para o filtro é de R$ 120,00. " + \
        "Logo pode aparecer um jogo de qualquer preço aqui."
    )
    msgList.append(
        "A faixa mínima de preço para o filtro é de R$ 10,00. " + \
        "Logo o jogo acima está nessa faixa."
    )

    return msgList