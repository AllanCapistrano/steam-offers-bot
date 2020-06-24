from catch_offers import CatchOffers
import asyncio
import discord
import discordToken

TOKEN = discordToken.myToken()
client = discord.Client()
color = 0xa82fd2
icon = "https://cdn.discordapp.com/app-icons/714852360241020929/b8dcc72cfc7708a4efd31787dceb5350.png?size=64"

@client.event
async def on_ready():
    print("\n{} está online".format(client.user.name))
    game = discord.Game("$help")
    online = discord.Status.online
    await client.change_presence(status = online, activity = game)

@client.event
async def on_message(message):
    if(message.content.lower().startswith("$help") or message.content.lower().startswith("$ajuda") or message.content.lower().startswith("$comandos")):
        embedHelp = discord.Embed(
            color = color
        )
        embedHelp.set_author(name = "SteamOffersBot lista de comandos:", icon_url = icon)
        embedHelp.add_field(name = "```$promocao``` ou ```$pr```", value = "**Exibe quais jogos estão na promoção diária da Steam ou gratuitos por um tempo limitado.**", inline = False)
        embedHelp.add_field(name = "```$destaque``` ou ```$dt```", value = "**Exibe os eventos que estão em destaque na Steam, ou os jogos em promoção que estão em destaque na loja.**", inline = False)
        embedHelp.add_field(name = "```$novidades``` ou ```$populares``` ou ```$np```", value = "**Exibe quais jogos da categoria \"Novidades Populares\" estão em promoção na loja.**", inline = False)
        embedHelp.add_field(name = "```$maisvendidos``` ou ```$mv```", value = "**Exibe quais jogos da categoria \"Mais Vendidos\" estão em promoção na loja.**", inline = False)
        embedHelp.add_field(name = "```$maisjogados``` ou ```$mj```", value = "**Exibe quais jogos da categoria \"Mais Jogados\" estão em promoção na loja.**", inline = False)
        embedHelp.add_field(name = "```$precompra``` ou ```$pc```", value = "**Exibe quais jogos da categoria \"Pré-compra\" estão em promoção na loja.**", inline = False)
        embedHelp.add_field(name = "```$convite```", value = "**Gera o convite para que o Bot possa ser adicionado em outros servidores.**", inline = False)
        embedHelp.add_field(name = "```$botinfo```", value = "**Exibe as informações do Bot.**", inline = False)

        await message.channel.send(embed = embedHelp)

    if(message.content.lower().startswith("$convite")):
        embedInvite = discord.Embed(
            title = "Aqui está o link para o convite:",
            color = color,
            description = "**https://discord.com/oauth2/authorize?client_id=714852360241020929&scope=bot&permissions=485440**"
        )
        embedInvite.set_thumbnail(url = icon)

        await message.channel.send(embed = embedInvite)

    if(message.content.lower().startswith("$destaque") or message.content.lower().startswith("$dt")):
        catchOffers = CatchOffers()
        list_gamesURl, list_gamesIMG, list_H2 = catchOffers.getSpotlightOffers()
        x = len(list_gamesURl)

        if(x == 0):
            await message.channel.send('😟 **Nenhum destaque encontrado no momento, tente novamente mais tarde!**')

        else:
            while(x > 0):
                embedSpotlightGames = discord.Embed(
                    title = "🎮 Jogo/Evento em Destaque 🎮",
                    color = color
                )
                embedSpotlightGames.set_image(url = list_gamesIMG[x - 1])
                embedSpotlightGames.add_field(name = "**Link:**", value = "**" + list_gamesURl[x - 1] + "**", inline = False)
                embedSpotlightGames.add_field(name = "**Descrição:**", value = "**" +  list_H2[x - 1] + "**", inline = False)
                
                await message.channel.send(embed = embedSpotlightGames)

                x = x - 1

    if(message.content.lower().startswith("$promocao") or message.content.lower().startswith("$pr")):
        catchOffers = CatchOffers()
        list_gamesURl, list_gamesIMG = catchOffers.getDailyGamesOffers()
        list_gamesOP, list_gamesFP = catchOffers.getDailyGamesOffersPrices()
        x = len(list_gamesURl)

        if(x == 0):
            await message.channel.send('😟 **Nenhuma promoção encontrada no momento, tente novamente mais tarde!**')

        else:
            while(x > 0):
                embedDailyGames = discord.Embed(
                    title = "🕹️ Oferta do Dia 🕹️",
                    color = color
                )
                embedDailyGames.set_image(url = list_gamesIMG[x - 1])
                embedDailyGames.add_field(name = "**Link:**", value = "**" + list_gamesURl[x - 1] + "**", inline = False)
                embedDailyGames.add_field(name = "**Preço Original:**", value = "**"+ list_gamesOP[x - 1] + "**", inline = True)
                embedDailyGames.add_field(name = "**Preço com Desconto:**", value = "**" + list_gamesFP[x - 1] + "**", inline = True)
                #Só há a necessidade do rodapé caso o jogo possua um preço disponível.
                if(list_gamesOP[x - 1] != "Não disponível!" and list_gamesFP[x - 1] != "Não disponível!"):
                    embedDailyGames.set_footer(text = "⚠️Atenção, os preços estão em Dólar") #Pois o Bot está rodando em uma máquina Norte America.

                await message.channel.send(embed = embedDailyGames)
                x = x - 1

    if(message.content.lower().startswith("$botinfo")):
        embedBotInfo = discord.Embed(
            title = "📊 Informações 📊",
            color = color
        )
        embedBotInfo.add_field(name = "Python", value = "**3.7.7**", inline = True)
        embedBotInfo.add_field(name = "discord.py", value = "**1.3.3**", inline = True)
        embedBotInfo.add_field(name = "Sobre SteamOffersBot", value = "**Bot feito para notificar os jogos que estão em promoção, sem a necessidade de abrir a Steam ou sair do Discord. Foi criado por ArticZ#1081**", inline = False)
        embedBotInfo.set_footer(text = "Criado em 26 de Maio de 2020!")

        await message.channel.send(embed = embedBotInfo)

    if(message.content.lower().startswith("$novidades") or message.content.lower().startswith("$populares") or message.content.lower().startswith("$np")):
        catchOffers = CatchOffers()
        list_gamesNames, list_gamesURL, list_gamesOriginalPrice, list_gamesFinalPrice = catchOffers.getTabContent('https://store.steampowered.com/specials#p=0&tab=NewReleases', 'NewReleasesRows')
        list_gamesNames.reverse(), list_gamesURL.reverse(), list_gamesOriginalPrice.reverse(), list_gamesFinalPrice.reverse()
        num = x = len(list_gamesNames)

        if(x == 0):
            await message.channel.send('😟 **Nenhuma promoção encontrada no momento, tente novamente mais tarde!**')

        else:
            messageConcat_1 = ''
            messageConcat_2 = ''
            member = message.author
            while(x > 0):
                if(x >= num/2):
                    messageConcat_1 = messageConcat_1 + "**Nome: **" + list_gamesNames[x - 1] + "\n**Link:** <" + list_gamesURL[x - 1] + ">" + "\n**Preço Original: **" + list_gamesOriginalPrice[x - 1] + "\n**Preço com Desconto: **" + list_gamesFinalPrice[x - 1] + "\n\n"
                else:
                    messageConcat_2 = messageConcat_2 + "**Nome: **" + list_gamesNames[x - 1] + "\n**Link:** <" + list_gamesURL[x - 1] + ">" + "\n**Preço Original: **" + list_gamesOriginalPrice[x - 1] + "\n**Preço com Desconto: **" + list_gamesFinalPrice[x - 1] + "\n\n"
                x = x - 1

            await message.channel.send(member.mention + "** Cheque sua DM** 😃")
            await member.send(messageConcat_1)
            await member.send(messageConcat_2)
            await member.send("\n**⚠️Atenção, os preços estão em Dólar**")

    if(message.content.lower().startswith("$maisvendidos") or message.content.lower().startswith("$mv")):
        catchOffers = CatchOffers()
        list_gamesNames, list_gamesURL, list_gamesOriginalPrice, list_gamesFinalPrice = catchOffers.getTabContent('https://store.steampowered.com/specials#p=0&tab=TopSellers', 'TopSellersRows')
        list_gamesNames.reverse(), list_gamesURL.reverse(), list_gamesOriginalPrice.reverse(), list_gamesFinalPrice.reverse()
        num = x = len(list_gamesNames)

        if(x == 0):
            await message.channel.send('😟 **Nenhuma promoção encontrada no momento, tente novamente mais tarde!**')

        else:
            messageConcat_1 = ''
            messageConcat_2 = ''
            member = message.author
            while(x > 0):
                if(x >= num/2):
                    messageConcat_1 = messageConcat_1 + "**Nome: **" + list_gamesNames[x - 1] + "\n**Link:** <" + list_gamesURL[x - 1] + ">" + "\n**Preço Original: **" + list_gamesOriginalPrice[x - 1] + "\n**Preço com Desconto: **" + list_gamesFinalPrice[x - 1] + "\n\n"
                else:
                    messageConcat_2 = messageConcat_2 + "**Nome: **" + list_gamesNames[x - 1] + "\n**Link:** <" + list_gamesURL[x - 1] + ">" + "\n**Preço Original: **" + list_gamesOriginalPrice[x - 1] + "\n**Preço com Desconto: **" + list_gamesFinalPrice[x - 1] + "\n\n"
                x = x - 1

            await message.channel.send(member.mention + "** Cheque sua DM** 😃")
            await member.send(messageConcat_1)
            await member.send(messageConcat_2)
            await member.send("\n**⚠️Atenção, os preços estão em Dólar**")

    if(message.content.lower().startswith("$maisjogados") or message.content.lower().startswith("$mj")):
        catchOffers = CatchOffers()
        list_gamesNames, list_gamesURL, list_gamesOriginalPrice, list_gamesFinalPrice = catchOffers.getTabContent('https://store.steampowered.com/specials#p=0&tab=ConcurrentUsers', 'ConcurrentUsersRows')
        list_gamesNames.reverse(), list_gamesURL.reverse(), list_gamesOriginalPrice.reverse(), list_gamesFinalPrice.reverse()
        num = x = len(list_gamesNames)

        if(x == 0):
            await message.channel.send('😟 **Nenhuma promoção encontrada no momento, tente novamente mais tarde!**')

        else:
            messageConcat_1 = ''
            messageConcat_2 = ''
            member = message.author
            while(x > 0):
                if(x >= num/2):
                    messageConcat_1 = messageConcat_1 + "**Nome: **" + list_gamesNames[x - 1] + "\n**Link:** <" + list_gamesURL[x - 1] + ">" + "\n**Preço Original: **" + list_gamesOriginalPrice[x - 1] + "\n**Preço com Desconto: **" + list_gamesFinalPrice[x - 1] + "\n\n"
                else:
                    messageConcat_2 = messageConcat_2 + "**Nome: **" + list_gamesNames[x - 1] + "\n**Link:** <" + list_gamesURL[x - 1] + ">" + "\n**Preço Original: **" + list_gamesOriginalPrice[x - 1] + "\n**Preço com Desconto: **" + list_gamesFinalPrice[x - 1] + "\n\n"
                x = x - 1

            await message.channel.send(member.mention + "** Cheque sua DM** 😃")
            await member.send(messageConcat_1)
            await member.send(messageConcat_2)
            await member.send("\n**⚠️Atenção, os preços estão em Dólar**")

    if(message.content.lower().startswith("$precompra") or message.content.lower().startswith("$pc")):
        catchOffers = CatchOffers()
        list_gamesNames, list_gamesURL, list_gamesOriginalPrice, list_gamesFinalPrice = catchOffers.getTabContent('https://store.steampowered.com/specials#p=0&tab=ComingSoon', 'ComingSoonRows')
        list_gamesNames.reverse(), list_gamesURL.reverse(), list_gamesOriginalPrice.reverse(), list_gamesFinalPrice.reverse()
        num = x = len(list_gamesNames)

        if(x == 0):
            await message.channel.send('😟 **Nenhuma promoção encontrada no momento, tente novamente mais tarde!**')

        else:
            messageConcat_1 = ''
            messageConcat_2 = ''
            member = message.author
            while(x > 0):
                if(x >= num/2):
                    messageConcat_1 = messageConcat_1 + "**Nome: **" + list_gamesNames[x - 1] + "\n**Link:** <" + list_gamesURL[x - 1] + ">" + "\n**Preço Original: **" + list_gamesOriginalPrice[x - 1] + "\n**Preço com Desconto: **" + list_gamesFinalPrice[x - 1] + "\n\n"
                else:
                    messageConcat_2 = messageConcat_2 + "**Nome: **" + list_gamesNames[x - 1] + "\n**Link:** <" + list_gamesURL[x - 1] + ">" + "\n**Preço Original: **" + list_gamesOriginalPrice[x - 1] + "\n**Preço com Desconto: **" + list_gamesFinalPrice[x - 1] + "\n\n"
                x = x - 1

            await message.channel.send(member.mention + "** Cheque sua DM** 😃")
            await member.send(messageConcat_1)
            await member.send(messageConcat_2)
            await member.send("\n**⚠️Atenção, os preços estão em Dólar**")

client.run(TOKEN)