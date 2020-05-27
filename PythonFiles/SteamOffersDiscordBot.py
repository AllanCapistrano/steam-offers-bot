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
    if(message.content.lower().startswith("$help")):
        embedHelp = discord.Embed(
            color = color
        )
        embedHelp.set_author(name = "SteamOffersBot lista de comandos:", icon_url = icon)
        embedHelp.add_field(name = "```$promocao```", value = "**Exibe quais jogos estão na promoção diária da Steam ou gratuitos por um tempo limitado.**", inline = False)
        embedHelp.add_field(name = "```$destaque```", value = "**Exibe os eventos que estão em destaque na Steam, ou os jogos em promoção que estão em destaque na loja.**", inline = False)
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

    if(message.content.lower().startswith("$destaque")):
        catchOffers = CatchOffers()
        list_gamesURl, list_gamesIMG, list_H2 = catchOffers.getSpotlightOffers()
        x = len(list_gamesURl)

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

    if(message.content.lower().startswith("$promocao")):
        catchOffers = CatchOffers()
        list_gamesURl, list_gamesIMG = catchOffers.getDailyGamesOffers()
        list_gamesOP, list_gamesFP = catchOffers.getDailyGamesOffersPrices()
        x = len(list_gamesURl)

        while(x > 0):
            embedDailyGames = discord.Embed(
                title = "🕹️ Oferta do Dia 🕹️",
                color = color
            )
            embedDailyGames.set_image(url = list_gamesIMG[x - 1])
            embedDailyGames.add_field(name = "**Link:**", value = "**" + list_gamesURl[x - 1] + "**", inline = False)
            embedDailyGames.add_field(name = "**Preço Original:**", value = "**US" + list_gamesOP[x - 1] + "**", inline = True)
            embedDailyGames.add_field(name = "**Preço com Desconto:**", value = "**US" + list_gamesFP[x - 1] + "**", inline = True)
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

client.run(TOKEN)