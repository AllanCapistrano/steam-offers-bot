from random import randint

PREFIX = "$"
IMG_GENRES = "https://i.imgur.com/q0NfeWX.png"

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
        "utilize o comando `{}help genre` para verificar ".format(PREFIX) + \
        "a lista completa dos gêneros disponíveis.**"
    )

    return msgList

def checkDm() -> list:
    """ Mensagem para as promoções que são enviadas para o privado.

    Returns
    -----------
    message: :class:`str`
    """
    
    return "** Cheque sua DM**"

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

    msgList.append("**[Clique Aqui]({}) para ver uma imagem com todos os possíveis gêneros.**".format(IMG_GENRES))
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
    msgList.append("**Mostra o resumo das análises de um jogo. Obs: Não precisa dos [].**")

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
        "Criado por ") # Informações.
    msgList.append("17 de Dezembro de 2021") # Data da última atualização.

    return msgList

def status(prefix: str, numServers: int) -> list:
    """ Mensagens de status do Bot.

    Returns
    -----------
    statusList: :class:`list`
    """
    
    statusList = []

    statusList.append("{}help | {} Servidores".format(prefix, numServers))
    statusList.append("{}help genre | {} Servidores".format(prefix, numServers))
    statusList.append("{}destaque | {} Servidores".format(prefix, numServers))
    statusList.append("{}promoção | {} Servidores".format(prefix, numServers))
    statusList.append("{}botinfo | {} Servidores".format(prefix, numServers))
    statusList.append("{}convite | {} Servidores".format(prefix, numServers))
    statusList.append("{}game [nome] | {} Servidores".format(prefix, numServers))
    statusList.append("{}genre [gênero] | {} Servidores".format(prefix, numServers))
    statusList.append("{}maxprice [preço] | {} Servidores".format(prefix, numServers))
    statusList.append("{}análises [nome] | {} Servidores".format(prefix, numServers))

    return statusList

def commandAlert() -> list:
    """ Mensagens de erro durante o envio de um comando.

    Returns
    -----------
    alertList: :class:`list`
    """
    
    alertList = []

    alertList.append("⚠️ **Informe o nome do jogo! Ex: `{}game undertale`**".format(PREFIX))
    alertList.append("⚠️ **Informe o gênero do jogo! Ex: `{}genre casual`**".format(PREFIX))
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

def gameGenres() -> str:
    """ Gêneros dos jogos.

    Returns
    -----------
    genres: :class:`str`
    """
    
    return "`Ação`, `Arcade e Ritmo`, `Luta e Artes Marciais`, `Plataformas e " + \
        "Corridas Intermináveis`, `Porradaria`, `Roguelike de Ação`, `Tiro em " + \
        "Terceira pessoa` ou `TPS`, `Tiro em Primeira Pessoa` ou `FPS`, `RPG`, " + \
        "`JRPG`, `RPG de Ação`, `RPG de Estratégia`, `RPGs de Aventura`, `RPGs em " + \
        "Grupos`, `RPGs em Turnos`, `Roguelike`, `Estratégia`, `Cidades e Colônias`, " + \
        "`Defesa de Torres`, `Estratégia Baseada em Turnos`, `Estratégia em Tempo " + \
        "Real` ou `RTS`, `Grande Estratégia e 4X`, `Militar`, `Tabuleiro e Cartas`, " + \
        "`Aventura e Casual`, `Aventura`, `Casuais`, `Metroidvania`, `Quebra-Cabeça`, " + \
        "`Romance Visual`, `Trama Excepcional`, `Simulador`, `Construção e Automação`, " + \
        "`Encontros`, `Espaço e Aviação`, `Física e Faça o que quiser`, `Gestão " + \
        "de Negócios`, `Rurais e de Fabricação`, `Vida e Imersivos`, `Esporte e " + \
        "Corrida`, `Corrida`, `Esporte em Equipe`, `Esportes`, `Esportes " + \
        "Individuais`, `Pescaria e Caça`, `Simuladores de Esporte`, `Simulação " + \
        "de Corrida`"

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
    msgList.append(
        "**É necessário informar uma faixa máxima de preço.**"
    )

    return msgList