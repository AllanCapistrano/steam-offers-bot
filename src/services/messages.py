from random import randint

class Message:
    def randomMessage(self, msg: list) -> str:
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

    def noOffers(self, prefix: str = None) -> list:
        """ Mensagens para quando não existem promoções ou jogos em destaque.

        Parameters
        -----------
        prefix: :class:`str`
            Prefixo utilizado pelo Bot.

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
            "utilize o comando `{}help genre` para verificar ".format(prefix) + \
            "a lista completa dos gêneros disponíveis.**"
        )

        return msgList

    def checkDm(self) -> list:
        """ Mensagem para as promoções que são enviadas para o privado.

        Returns
        -----------
        message: :class:`str`
        """
        
        return "** Cheque sua DM**"

    def title(self, genre: str = None , gameName: str = None) -> list:
        """ Títulos das embeds.

        Parameters
        -----------
        genre: :class:`str`
            Gênero do jogo.
        gameName: :class:`str`
            Nome do jogo.

        Returns
        -----------
        titleList: :class:`list`
        """
        
        titleList = []

        titleList.append("Aqui está o link para o convite:") # $invite ou $convite
        titleList.append("🎮 Jogo/Evento em Destaque 🎮") # $destaque ou $dt
        titleList.append("🕹️ Oferta do Dia 🕹️") # $promocao ou $pr
        titleList.append("📊 Informações 📊") # $botinfo ou $info
        titleList.append("🎮 Gêneros dos Jogos 🕹️") # $help genre

        titleList.append("👾 Jogo: {} 👾".format(gameName)) # $game
        
        # $genre
        if(genre == "casual" or genre == "indie" or genre == "multijogador massivo" or genre == "rpg"):
            titleList.append("🎮 Jogo __{}__ recomendado 🕹️".format(genre))
        else:
            titleList.append("🎮 Jogo de __{}__ recomendado 🕹️".format(genre))

        
        titleList.append("💰 Jogo: {} 💰".format(gameName)) # $maxprice

        return titleList

    def helpValues(self, img: str = None, prefix = None) -> list:
        """ Conteúdo do comando $help.

        Parameters
        -----------
        genre: :class:`str`
            Link da imagem que contém os a lista de gêneros dos jogos.
        prefix: :class:`str`
            Prefixo utilizado pelo Bot.

        Returns
        -----------
        msgList: :class:`list`
        """
        
        msgList = []

        msgList.append("**[Clique Aqui]({}) para ver uma imagem com todos os possíveis gêneros.**".format(img))
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
        msgList.append("**Envia para a sua DM uma lista contendo diversos jogos. Obs: digite `{}help gametab` para ver todas as categorias.**".format(prefix)
        )

        return msgList

    def infoValues(self) -> list:
        """ Conteúdo do comando $botinfo.

        Returns
        -----------
        msgList: :class:`list`
        """
        
        msgList = []

        msgList.append("**3.10.1**") # Versão Python
        msgList.append("**1.7.3**") # Versão Discord.py
        msgList.append("**Bot para visualizar informações sobre jogos e promoções "
            "na Steam sem precisar sair do Discord. Criado por ") # Informações.
        msgList.append("15 de Janeiro de 2022") # Data da última atualização.

        return msgList

    def status(self, prefix: str, numServers: int) -> list:
        """ Mensagens de status do Bot.

        Parameters
        -----------
        prefix: :class:`str`
            Prefixo utilizado pelo Bot.
        numServers: :class:`int`
            Quantidade de servidores em que o Bot está presente.

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
        statusList.append("{}análise [nome] | {} Servidores".format(prefix, numServers))

        return statusList

    def commandAlert(self, prefix: str = None) -> list:
        """ Mensagens de erro durante o envio de um comando.

        Parameters
        -----------
        prefix: :class:`str`
            Prefixo utilizado pelo Bot.

        Returns
        -----------
        alertList: :class:`list`
        """
        
        alertList = []

        alertList.append("⚠️ **Informe o nome do jogo! Ex: `{}game undertale`**".format(prefix))
        alertList.append("⚠️ **Informe o gênero do jogo! Ex: `{}genre casual`**".format(prefix))
        alertList.append("⚠️ **Comando inválido!**")

        return alertList

    def wrongGame(self, url: str) -> str:
        """ Mensagem de erro ao buscar um jogo específico.

        Parameters
        -----------
        url: :class:`str`
            Url para ver a lista completa dos jogos.

        Returns
        -----------
        message: :class:`srt`
        """

        return "Não era o jogo que estava buscando? [Clique Aqui]({}) para " +\
        "visualizar a lista completa dos jogos.".format(url)

    def gameGenres(self) -> str:
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

    def searchMessage(self) -> list:
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

    def recommendationByPrice(self) -> list:
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

    def noReviews(self) -> list:
        """ Mensagens para quando não análises para um jogo.

        Returns
        -----------
        msgList: :class:`list`
        """
        
        msgList = []

        msgList.append("Não há análises disponíveis no momento.")

        return msgList
