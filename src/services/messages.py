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

    def noOffers(self, language: str = None, prefix: str = None) -> list:
        """ Mensagens para quando não existem promoções ou jogos em destaque.

        Parameters
        -----------
        language: :class:`str`
            Idioma do comando.
        prefix: :class:`str`
            Prefixo utilizado pelo Bot.

        Returns
        -----------
        msgList: :class:`list`
        """

        msgList = []

        if(language == None):
            # Mensagem de destaque.
            msgList.append(
                "😟 **Nenhum destaque encontrado no momento, tente novamente mais tarde!**")
            # Mensagem de promoção.
            msgList.append(
                "😟 **Nenhuma promoção encontrada no momento, tente novamente mais tarde!**")
            # Mensagem de jogo específico.
            msgList.append(
                "😟 **Jogo não encontrado! Por favor verifique o nome digitado.**"
            )
            # Mensagem de gênero do jogo.
            msgList.append(
                "😟 **Gênero não encontrado! Por favor verifique o gênero foi digitado ou " + \
                "utilize o comando `{}ajuda gênero` para verificar ".format(prefix) + \
                "a lista completa dos gêneros disponíveis.**"
            )
        elif(language == "english"):
            # Mensagem de destaque.
            msgList.append(
                "😟 **Can't find spotlights at the moment, try again later!**")
            # Mensagem de promoção.
            msgList.append(
                "😟 **Can't find daily deals at the moment, try again later!**")
            # Mensagem de jogo específico.
            msgList.append(
                "😟 **Game not found! Please check the name entered.**"
            )
            # Mensagem de gênero do jogo.
            msgList.append(
                "😟 **Genre not found! Please check the genre entered or " + \
                "try `{}help genre` to see the full list of available game genres.**".format(prefix)
            )

        return msgList

    def checkDm(self, language: str = None) -> list:
        """ Mensagem para as promoções que são enviadas para o privado.

        Parameters
        -----------
        language: :class:`str`
            Idioma do comando.

        Returns
        -----------
        message: :class:`str`
        """
        if(language == None):
            return "** Cheque sua DM**"
        elif(language == "english"):
            return "** Check your DM**"

    def title(self, language: str = None, genre: str = None , gameName: str = None) -> list:
        """ Títulos das embeds.

        Parameters
        -----------
        language: :class:`str`
            Idioma do comando.
        genre: :class:`str`
            Gênero do jogo.
        gameName: :class:`str`
            Nome do jogo.

        Returns
        -----------
        titleList: :class:`list`
        """
        
        titleList = []

        if(language == None):
            titleList.append("Aqui está o link para o convite:") # $convite
            titleList.append("🎮 Jogo/Evento em Destaque 🎮") # $destaque ou $dt
            titleList.append("🕹️ Oferta do Dia 🕹️") # $promocao ou $pr
            titleList.append("📊 Informações 📊") # $botinfo
            titleList.append("🎮 Gêneros dos Jogos 🕹️") # $ajuda gênero
            titleList.append("👾 Jogo: {} 👾".format(gameName)) # $jogo
            
            # $genre
            if(genre == "casual" or genre == "indie" or genre == "multijogador massivo" or genre == "rpg"):
                titleList.append("🎮 Jogo __{}__ recomendado 🕹️".format(genre))
            else:
                titleList.append("🎮 Jogo de __{}__ recomendado 🕹️".format(genre))

            titleList.append("💰 Jogo: {} 💰".format(gameName)) # $preçomáximo
            titleList.append("💵 Moedas Disponíveis 💵") # $ajuda moedas
        elif(language == "english"):
            titleList.append("Here is the link to invite:") # $invite
            titleList.append("🎮 Spotlight 🎮") # $spotlight or $sl
            titleList.append("🕹️ Daily Deal 🕹️") # $dailydeal or $dd
            titleList.append("📊 Information 📊") # $info
            titleList.append("🎮 Game Genres 🕹️") # $help genre
            titleList.append("👾 Game: {} 👾".format(gameName)) # $game
            titleList.append("🎮 Recommended __{}__ game  🕹️".format(genre)) # $genre
            titleList.append("💰 Game: {} 💰".format(gameName)) # $maxprice
            titleList.append("💵 Supported Currencies 💵") # $help currency

        return titleList

    def helpValues(self, language: str = None, img: str = None, prefix = None) -> list:
        """ Conteúdo do comando $help.

        Parameters
        -----------
        language: :class:`str`
            Idioma do comando.
        genre: :class:`str`
            Link da imagem que contém os a lista de gêneros dos jogos.
        prefix: :class:`str`
            Prefixo utilizado pelo Bot.

        Returns
        -----------
        msgList: :class:`list`
        """
        
        msgList = []

        if(language == None):
            msgList.append("**[Clique Aqui]({}) para ver uma imagem com todos os possíveis gêneros.**".format(img))
            msgList.append("**Exibe quais jogos estão na promoção diária da Steam ou gratuitos por um tempo limitado.**")
            msgList.append("**Exibe os eventos que estão em destaque na Steam, ou os jogos em promoção que estão em destaque na loja.**")
            msgList.append("**Exibe quais jogos da categoria \"Novidades Populares\" estão em promoção na loja.**")
            msgList.append("**Exibe quais jogos da categoria \"Mais Vendidos\" estão em promoção na loja.**")
            msgList.append("**Exibe quais jogos da categoria \"Mais Jogados\" estão em promoção na loja.**")
            msgList.append("**Exibe quais jogos da categoria \"Pré-compra\" estão em promoção na loja.**")
            msgList.append("**Gera o convite para que o Bot possa ser adicionado em outros servidores.**")
            msgList.append("**Exibe as informações do Bot.**")
            msgList.append("**Busca um jogo pelo nome e exibe as suas informações. Obs: Não precisa dos [].**")
            msgList.append("**Recomenda um jogo a partir do gênero especificado. Obs: Não precisa dos [].**")
            msgList.append("**Recomenda um jogo dada uma faixa máxima de preço. Obs: Não precisa dos [].**")
            msgList.append("**Mostra o resumo das análises de um jogo. Obs: Não precisa dos [].**")
            msgList.append("**Envia para a sua DM uma lista contendo diversos jogos. Obs: Digite `{}ajuda categoria` para ver todas as categorias.**".format(prefix))
            msgList.append("**Mostra todas as moedas disponíveis.**")
        elif(language == "english"):
            msgList.append("**[Click Here]({}) to see an image with all game genres.**".format(img))
            msgList.append("**Shows which games are on daily offer or free to play.**")
            msgList.append("**Shows which events or games are in the spotlight in the Steam.**")
            msgList.append("**Shows which games in the \"New & Trending\" category are on sale.**")
            msgList.append("**Shows which games in the \"Top Sellers\" category are on sale.**")
            msgList.append("**Shows which games in the \"What's Being Played\" category are on sale.**")
            msgList.append("**Shows which games in the \"Pre-Purchase\" category are on sale.**")
            msgList.append("**Generate the bot invite.**")
            msgList.append("**Show information about the bot.**")
            msgList.append("**Search for a game by name. Ps: Don't need the [].**")
            msgList.append("**Recommends a game by genre. Ps: Don't need the [].**")
            msgList.append("**Recommends a game by price range. Ps: Don't need the [].**")
            msgList.append("**Shows a summary of the reviews about the game. Ps: Don't need the [].**")
            msgList.append("**Send to you a private message with a list of games. PS: To see all categories, send `{}help gametab`**".format(prefix))
            msgList.append("**Shows all the currencies you can use.**")

        return msgList

    def infoValues(self, language: str = None) -> list:
        """ Conteúdo do comando $botinfo.

        Returns
        -----------
        msgList: :class:`list`
        """
        
        msgList = []

        msgList.append("**3.10.5**") # Versão Python
        msgList.append("**2.0.0**") # Versão Discord.py

        if(language == None):
            msgList.append("**Bot para visualizar informações sobre jogos e promoções "
                "na Steam sem precisar sair do Discord. Criado por ") # Informações.
            msgList.append("21 de Agosto de 2022") # Data da última atualização.
        elif(language == "english"):
            msgList.append("**Bot to show information about Steam games and "
                "offers, without leaving Discord. Created by ") # Informações.
            msgList.append("August 21, 2022") # Data da última atualização.

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

        statusList.append("{}ajuda | {} Servidores".format(prefix, numServers))
        statusList.append("{}help | {} Servers".format(prefix, numServers))

        return statusList

    def commandAlert(self, language: str = None, prefix: str = None, command: str = None, status: str = None) -> list:
        """ Mensagens de erro durante o envio de um comando.

        Parameters
        -----------
        language: :class:`str`
            Idioma do comando.
        prefix: :class:`str`
            Prefixo utilizado pelo Bot.
        command :class:`str`
            Comando utilizado.
        status :class:`str`
            Estado do comando.

        Returns
        -----------
        alertList: :class:`list`
        """
        
        alertList = []

        if(language == None):
            alertList.append("⚠️ **Informe o nome do jogo! Ex: `{}jogo undertale`**".format(prefix))
            alertList.append("⚠️ **Informe o gênero do jogo! Ex: `{0}gênero casual` \n Ou digite `{0}help genre` para ver todos os gêneros.**".format(prefix))
            alertList.append("⚠️ **Comando inválido!**")
            alertList.append("⚠️ **Categoria inválida! \nDigite `{0}ajuda categoria` para ver todas as categorias.**".format(prefix))
            alertList.append("⚠️ **Informe o nome do jogo! Ex: `{}análise undertale`**".format(prefix))
            alertList.append("⚠️ **Comando desabilitado temporariamente!**")
            alertList.append("⚠️ **Não consegui encontrar o comando especificado!**")
            alertList.append("⚠️ **Erro! Você não pode desabilitar este comando.**")
        elif(language == "english"):
            alertList.append("⚠️ **You need to pass the name of the game! Ex: `{}game undertale`**".format(prefix))
            alertList.append("⚠️ **You need to pass the genre of the game! Ex: `{0}genre casual` \n Or try `{0}help genre` to see all genres.**".format(prefix))
            alertList.append("⚠️ **Invalid command!**")
            alertList.append("⚠️ **Invalid category! \nTry `{0}help gametab` to see all categories.**".format(prefix))
            alertList.append("⚠️ **You need to pass the name of the game! Ex: `{}review undertale`**".format(prefix))
            alertList.append("⚠️ **Command temporarily disabled!**")
            alertList.append("⚠️ **I can't find this command!**")
            alertList.append("⚠️ **Error! You can't disable this command.**")

        alertList.append(f"⚠️ **Comando `{prefix}{command}` {status} com sucesso.**")

        return alertList

    def wrongGame(self, url: str, language: str = None) -> str:
        """ Mensagem de erro ao buscar um jogo específico.

        Parameters
        -----------
        url: :class:`str`
            Url para ver a lista completa dos jogos.

        Returns
        -----------
        message: :class:`srt`
        """
        if(language == None):
            return "Não era o jogo que estava buscando? [Clique Aqui]({}) para visualizar a lista completa dos jogos.".format(url)
        elif(language == "english"):
            return "Not a game you're looking for? [Click Here]({}) to see the full list of games.".format(url)

    def gameGenres(self, language: str = None) -> str:
        """ Gêneros dos jogos.

        Parameters
        -----------
        language: :class:`str`
            Idioma do comando.

        Returns
        -----------
        genres: :class:`str`
        """
        if(language == None):
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
        elif(language == "english"):
            return "`Action`, `Action Rogue-Like`, `Arcade & Rythm`, `Beat 'Em Up`, " + \
                "`Fight & Martial Arts`, `First-Person Shooter`, `Platformer & Runner`, " + \
                "`Third-Person Shooter`, `Role-Playing`, `Action RPG`, `Adventure RPG`, " + \
                "`JRPG`, `Party-Based`, `Rogue-Like`, `Strategy RPG`, `Turn-Based`, " + \
                "`Card & Board`, `City & Sttlement`, `Grand & 4X`, `Military`, " + \
                "`Real-Time Strategy`, `Tower Defense`, `Turn-Based Strategy`, " + \
                "`Adventure & Casual`, `Adventure`, `Casual`, `Metroidvania`, `Puzzle`, " + \
                "`Story-Rich`, `Visual Novel`, `Simulation`, `Building & Automation`, " + \
                "`Business & Tycoon`, `Dating`, `Farming & Crafting`, `Life & Immersive`, " + \
                "`Sandbox & Physics`, `Space & Flight`, `Sport & Racing`, `All Sports`, " + \
                "`Fishing & Hunting`, `Individual Sports`, `Racing`, `Racing Sim`, " + \
                "`Sports Sim`, `Tema Sports`,"

    def searchMessage(self, language: str = None) -> list:
        """ Mensagens de busca.

        Parameters
        -----------
        language: :class:`str`
            Idioma do comando.

        Returns
        -----------
        msgList: :class:`list`
        """
        
        msgList = []

        if(language == None):
            msgList.append("**🔎 Procurando.**")
            msgList.append("**🔎 Procurando pelo jogo")
            msgList.append("**🔎 Procurando por um jogo do gênero")
            msgList.append("**🔎 Procurando por um jogo de até __R$")
        elif(language == "english"):
            msgList.append("**🔎 Searching.**")
            msgList.append("**🔎 Searching for the game")
            msgList.append("**🔎 Searching for a game of the genre")
            msgList.append("**🔎 Searching for a game of up to __$")

        return msgList

    def recommendationByPrice(self, language: str = None) -> list:
        """ Mensagens de recomendação de jogo por preço.

        Parameters
        -----------
        language: :class:`str`
            Idioma do comando.

        Returns
        -----------
        msgList: :class:`list`
        """
        
        msgList = []

        if(language == None):
            msgList.append(
                "⚠️ **Faixa de preço inválida! Tente novamente. " + \
                "\nObs: Não utilize vírgulas nem pontos.**"
            )
            msgList.append(
                "A faixa máxima de preço para o filtro é de R$ 120,00. " + \
                "Logo o jogo acima está em qualquer faixa de preço."
            )
            msgList.append(
                "A faixa mínima de preço para o filtro é de R$ 10,00. " + \
                "Logo o jogo acima está nessa faixa."
            )
            msgList.append(
                "⚠️ **É necessário informar uma faixa máxima de preço.**"
            )
        elif(language == "english"):
            msgList.append(
                "⚠️ **Invalid price range! Try again. " + \
                "\n PS: Don't use points or commas.**"
            )
            msgList.append(
                "The highest price range is $120.00. " + \
                "So the above game can be in any price range."
            )
            msgList.append(
                "The lowest price range is $10.00. " + \
                "So the above game is in this price range."
            )
            msgList.append(
                "**⚠️ Maximum price range is required.**"
            )

        return msgList

    def noReviews(self, language: str = None) -> list:
        """ Mensagens para quando não análises para um jogo.

        Parameters
        -----------
        language: :class:`str`
            Idioma do comando.

        Returns
        -----------
        msgList: :class:`list`
        """
        
        msgList = []

        if(language == None):
            msgList.append("Não há análises disponíveis no momento.")
        elif(language == "english"):
            msgList.append("No reviews available.")

        return msgList

    def somethingWentWrong(self, language: str = None) -> list:
        """ Mensagens para algo deu errado.

        Parameters
        -----------
        language: :class:`str`
            Idioma do comando.

        Returns
        -----------
        msgList: :class:`list`
        """
        
        msgList = []

        if(language == None):
            msgList.append("😞 **Algo de errado aconteceu! Tente novamente.**")
        elif(language == "english"):
            msgList.append("😞 **Something went wrong! Try again.**")

        return msgList

    def helpCurrencies(self, language: str = None) -> list:
        """ Conteúdo do comando $help currency.

        Parameters
        -----------
        language: :class:`str`
            Idioma do comando.

        Returns
        -----------
        msgList: :class:`list`
        """
        
        msgList = []

        if(language == None):
            msgList.append("Dirham")
            msgList.append("Peso (Argentina)")
            msgList.append("Dólar (Austrália)")
            msgList.append("Real (Brasil)")
            msgList.append("Dólar (Canadá)")
            msgList.append("Franco (Suíça)")
            msgList.append("Peso (Chile)")
            msgList.append("Chinese Renminbi (yuan)")
            msgList.append("Peso (Colômbia)")
            msgList.append("Cólon (Costa Rica)")
            msgList.append("Euro (União Europeia)")
            msgList.append("Libra (Reino Unido)")
            msgList.append("Dólar (Hong Kong)")
            msgList.append("Novo shekel (Israel)")
            msgList.append("Rupia (Indonésia)")
            msgList.append("Rupia (Índia)")
            msgList.append("Iene (Japão)")
            msgList.append("Won (Coreia do Sul)")
            msgList.append("Dinar (Kuwait)")
            msgList.append("Tenge (Cazaquistão)")
            msgList.append("Peso (México)")
            msgList.append("Ringuite (Malásia)")
            msgList.append("Coroa (Noruega)")
            msgList.append("Dólar (Nova Zelândia)")
            msgList.append("Sol (Peru)")
            msgList.append("Peso (Filipinas)")
            msgList.append("Złoty (Polônia)")
            msgList.append("Rial (Catar)")
            msgList.append("Rublo (Rússia)")
            msgList.append("Rial (Arábia Saudita)")
            msgList.append("Dólar (Singapura)")
            msgList.append("Baht (Tailândia)")
            msgList.append("Lira (Turquia)")
            msgList.append("Dólar (Taiwan)")
            msgList.append("Grívnia (Ucrânia)")
            msgList.append("Dólar (Estados Unidos)")
            msgList.append("Peso (Uruguai)")
            msgList.append("Dong (Vietnã)")
            msgList.append("Rande (África do Sul)")
        elif(language == "english"):
            msgList.append("United Arab Emirates Dirham")
            msgList.append("Argentine Peso")
            msgList.append("Australian Dollars")
            msgList.append("Brazilian Reals")
            msgList.append("Canadian Dollars")
            msgList.append("Swiss Francs")
            msgList.append("Chilean Peso")
            msgList.append("Chinese Renminbi (yuan)")
            msgList.append("Colombian Peso")
            msgList.append("Costa Rican Colón")
            msgList.append("European Union Euro")
            msgList.append("United Kingdom Pound")
            msgList.append("Hong Kong Dollar")
            msgList.append("Israeli New Shekel")
            msgList.append("Indonesian Rupiah")
            msgList.append("Indian Rupee")
            msgList.append("Japanese Yen")
            msgList.append("South Korean Won")
            msgList.append("Kuwaiti Dinar")
            msgList.append("Kazakhstani Tenge")
            msgList.append("Mexican Peso")
            msgList.append("Malaysian Ringgit")
            msgList.append("Norwegian Krone")
            msgList.append("New Zealand Dollar")
            msgList.append("Peruvian Sol")
            msgList.append("Philippine Peso")
            msgList.append("Polish Złoty")
            msgList.append("Qatari Riyal")
            msgList.append("Russian Rouble")
            msgList.append("Saudi Riyal")
            msgList.append("Singapore Dollar")
            msgList.append("Thai Baht")
            msgList.append("Turkish Lira")
            msgList.append("New Taiwan Dollar")
            msgList.append("Ukrainian Hryvnia")
            msgList.append("United States Dollar")
            msgList.append("Uruguayan Peso")
            msgList.append("Vietnamese Dong")
            msgList.append("South African Rand")

        return msgList

    def currenciesValues(self) -> list:
        """ Conteúdo do comando $help currency.

        Returns
        -----------
        currencyList: :class:`list`
        """
        
        currencyList = []

        currencyList.append("AED")
        currencyList.append("ARS")
        currencyList.append("AUD")
        currencyList.append("BRL")
        currencyList.append("CAD")
        currencyList.append("CHF")
        currencyList.append("CLP")
        currencyList.append("CNY")
        currencyList.append("COP")
        currencyList.append("CRC")
        currencyList.append("EUR")
        currencyList.append("GBP")
        currencyList.append("HKD")
        currencyList.append("ILS")
        currencyList.append("IDR")
        currencyList.append("INR")
        currencyList.append("JPY")
        currencyList.append("KRW")
        currencyList.append("KWD")
        currencyList.append("KZT")
        currencyList.append("MXN")
        currencyList.append("MYR")
        currencyList.append("NOK")
        currencyList.append("NZD")
        currencyList.append("PEN")
        currencyList.append("PHP")
        currencyList.append("PLN")
        currencyList.append("QAR")
        currencyList.append("RUB")
        currencyList.append("SAR")
        currencyList.append("SGD")
        currencyList.append("THB")
        currencyList.append("TRY")
        currencyList.append("TWD")
        currencyList.append("UAH")
        currencyList.append("USD")
        currencyList.append("UYU")
        currencyList.append("VND")
        currencyList.append("ZAR")

        return currencyList