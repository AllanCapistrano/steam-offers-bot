import asyncio
import discord
import time

from myUtils.catch_offers import CatchOffers
from myUtils import messages
from myUtils import discordToken

COLOR = 0xa82fd2
ICON = "https://cdn.discordapp.com/app-icons/714852360241020929/b8dcc72cfc7708a4efd31787dceb5350.png?size=64"
INVITE = "https://discord.com/oauth2/authorize?client_id=714852360241020929&scope=bot&permissions=485440"
URL = "https://store.steampowered.com/specials#p=0&tab="
TOKEN = discordToken.myToken()

client = discord.Client()
catchOffers = CatchOffers()


@client.event
async def on_ready():
    numServers = len(client.guilds)

    print("\n{} está online em {} servidores".format(client.user.name, numServers))

    game = discord.Game("Online em {} Servidores".format(numServers))
    online = discord.Status.online

    await client.change_presence(status=online, activity=game)


@client.event
async def on_message(message):
    # Comando: $help ou $ajuda ou $comandos
    if(message.content.lower().startswith("$help") or message.content.lower().startswith("$ajuda") or message.content.lower().startswith("$comandos")):
        embedHelp = discord.Embed(
            color=COLOR
        )
        embedHelp.set_author(
            name="SteamOffersBot lista de comandos:", icon_url=ICON)
        embedHelp.add_field(name="```$promocao``` ou ```$pr```",
                            value=messages.helpValues()[0], inline=False)
        embedHelp.add_field(name="```$destaque``` ou ```$dt```",
                            value=messages.helpValues()[1], inline=False)
        embedHelp.add_field(name="```$novidades``` ou ```$populares``` ou ```$np```",
                            value=messages.helpValues()[2], inline=False)
        embedHelp.add_field(name="```$maisvendidos``` ou ```$mv```",
                            value=messages.helpValues()[3], inline=False)
        embedHelp.add_field(name="```$maisjogados``` ou ```$mj```",
                            value=messages.helpValues()[4], inline=False)
        embedHelp.add_field(name="```$precompra``` ou ```$pc```",
                            value=messages.helpValues()[5], inline=False)
        embedHelp.add_field(name="```$convite```",
                            value=messages.helpValues()[6], inline=False)
        embedHelp.add_field(name="```$botinfo```",
                            value=messages.helpValues()[7], inline=False)
        embedHelp.add_field(name="```$game [nome do jogo]```",
                            value=messages.helpValues()[8], inline=False)

        await message.channel.send(embed=embedHelp)

    # Comando: $convite
    if(message.content.lower().startswith("$convite")):
        embedInvite = discord.Embed(
            title=messages.title()[0],
            color=COLOR,
            description='**{}**'.format(INVITE)
        )
        embedInvite.set_thumbnail(url=ICON)

        await message.channel.send(embed=embedInvite)

    # Comando: $destaque ou $dt
    if(message.content.lower().startswith("$destaque") or message.content.lower().startswith("$dt")):
        list_gamesURl, list_gamesIMG, list_H2 = catchOffers.getSpotlightOffers()
        x = len(list_gamesURl)

        if(x == 0):
            await message.channel.send(messages.noOffers()[0])

        else:
            while(x > 0):
                embedSpotlightGames = discord.Embed(
                    title=messages.title()[1],
                    color=COLOR
                )
                embedSpotlightGames.set_image(url=list_gamesIMG[x - 1])
                embedSpotlightGames.add_field(
                    name="**Link:**", value="**[Clique Aqui]({})**".format(list_gamesURl[x - 1]), inline=False)
                embedSpotlightGames.add_field(
                    name="**Descrição:**", value="**{}**".format(list_H2[x - 1]), inline=False)

                await message.channel.send(embed=embedSpotlightGames)

                x = x - 1

    # Comando: $promocao ou $pr
    if(message.content.lower().startswith("$promocao") or message.content.lower().startswith("$pr")):
        list_gamesURl, list_gamesIMG = catchOffers.getDailyGamesOffers()
        list_gamesOP, list_gamesFP = catchOffers.getDailyGamesOffersPrices()
        x = len(list_gamesURl)

        if(x == 0):
            await message.channel.send(messages.noOffers()[1])

        else:
            while(x > 0):
                embedDailyGames = discord.Embed(
                    title=messages.title()[2],
                    color=COLOR
                )
                embedDailyGames.set_image(url=list_gamesIMG[x - 1])
                embedDailyGames.add_field(
                    name="**Link:**", value="**[Clique Aqui]({})**".format(list_gamesURl[x - 1]), inline=False)
                embedDailyGames.add_field(
                    name="**Preço Original:**", value="**{}**".format(list_gamesOP[x - 1]), inline=True)
                embedDailyGames.add_field(
                    name="**Preço com Desconto:**", value="**{}**".format(list_gamesFP[x - 1]), inline=True)
                # Só há a necessidade do rodapé caso o jogo possua um preço disponível.
                if(list_gamesOP[x - 1] != "Não disponível!" and list_gamesFP[x - 1] != "Não disponível!"):
                    # Pois o Bot está rodando em uma máquina Norte America.
                    embedDailyGames.set_footer(
                        text=messages.currencyAlert())

                await message.channel.send(embed=embedDailyGames)
                x = x - 1

    # Comando: $botinfo
    if(message.content.lower().startswith("$botinfo")):
        embedBotInfo = discord.Embed(
            title=messages.title()[3],
            color=COLOR
        )
        embedBotInfo.add_field(name="Python", value=messages.infoValues()[0], inline=True)
        embedBotInfo.add_field(name="discord.py", value=messages.infoValues()[1], inline=True)
        embedBotInfo.add_field(name="Sobre SteamOffersBot", value=messages.infoValues()[2], inline=False)
        embedBotInfo.set_footer(text="Criado em 26 de Maio de 2020! | Última atualização em {}."
            .format(messages.infoValues()[3]))

        await message.channel.send(embed=embedBotInfo)

    # Comando: $novidades ou $populares ou $np
    if(message.content.lower().startswith("$novidades") or message.content.lower().
      startswith("$populares") or message.content.lower().startswith("$np")):
        list_gamesNames, list_gamesURL, list_gamesOriginalPrice, list_gamesFinalPrice = catchOffers.getTabContent(
            URL+'=NewReleases', 'NewReleasesRows')
        list_gamesNames.reverse(), list_gamesURL.reverse(
        ), list_gamesOriginalPrice.reverse(), list_gamesFinalPrice.reverse()
        num = x = len(list_gamesNames)

        if(x == 0):
            await message.channel.send(messages.noOffers()[1])

        else:
            messageConcat_1 = ''
            messageConcat_2 = ''
            member = message.author
            while(x > 0):
                if(x >= num/2):
                    messageConcat_1 = messageConcat_1 + "**Nome: **" + list_gamesNames[x - 1] + "\n**Link:** <" + list_gamesURL[x - 1] + ">" + \
                        "\n**Preço Original: **" + \
                        list_gamesOriginalPrice[x - 1] + "\n**Preço com Desconto: **" + \
                        list_gamesFinalPrice[x - 1] + "\n\n"
                else:
                    messageConcat_2 = messageConcat_2 + "**Nome: **" + list_gamesNames[x - 1] + "\n**Link:** <" + list_gamesURL[x - 1] + ">" + \
                        "\n**Preço Original: **" + \
                        list_gamesOriginalPrice[x - 1] + "\n**Preço com Desconto: **" + \
                        list_gamesFinalPrice[x - 1] + "\n\n"
                x = x - 1

            await message.channel.send(member.mention + messages.checkDm())
            await member.send(messageConcat_1)
            await member.send(messageConcat_2)
            await member.send("\n**{}**".format(messages.currencyAlert()))

    # Comando: $maisvendidos ou $mv
    if(message.content.lower().startswith("$maisvendidos") or message.content.lower().startswith("$mv")):
        list_gamesNames, list_gamesURL, list_gamesOriginalPrice, list_gamesFinalPrice = catchOffers.getTabContent(
            URL+'=TopSellers', 'TopSellersRows')
        list_gamesNames.reverse(), list_gamesURL.reverse(
        ), list_gamesOriginalPrice.reverse(), list_gamesFinalPrice.reverse()
        num = x = len(list_gamesNames)

        if(x == 0):
            await message.channel.send(messages.noOffers()[1])

        else:
            messageConcat_1 = ''
            messageConcat_2 = ''
            member = message.author
            while(x > 0):
                if(x >= num/2):
                    messageConcat_1 = messageConcat_1 + "**Nome: **" + list_gamesNames[x - 1] + "\n**Link:** <" + list_gamesURL[x - 1] + ">" + \
                        "\n**Preço Original: **" + \
                        list_gamesOriginalPrice[x - 1] + "\n**Preço com Desconto: **" + \
                        list_gamesFinalPrice[x - 1] + "\n\n"
                else:
                    messageConcat_2 = messageConcat_2 + "**Nome: **" + list_gamesNames[x - 1] + "\n**Link:** <" + list_gamesURL[x - 1] + ">" + \
                        "\n**Preço Original: **" + \
                        list_gamesOriginalPrice[x - 1] + "\n**Preço com Desconto: **" + \
                        list_gamesFinalPrice[x - 1] + "\n\n"
                x = x - 1

            await message.channel.send(member.mention + messages.checkDm())
            await member.send(messageConcat_1)
            await member.send(messageConcat_2)
            await member.send("\n**{}**".format(messages.currencyAlert()))

    # Comando: $maisjogados ou $mj
    if(message.content.lower().startswith("$maisjogados") or message.content.lower().startswith("$mj")):
        list_gamesNames, list_gamesURL, list_gamesOriginalPrice, list_gamesFinalPrice = catchOffers.getTabContent(
            URL+'=ConcurrentUsers', 'ConcurrentUsersRows')
        list_gamesNames.reverse(), list_gamesURL.reverse(
        ), list_gamesOriginalPrice.reverse(), list_gamesFinalPrice.reverse()
        num = x = len(list_gamesNames)

        if(x == 0):
            await message.channel.send(messages.noOffers()[1])

        else:
            messageConcat_1 = ''
            messageConcat_2 = ''
            member = message.author
            while(x > 0):
                if(x >= num/2):
                    messageConcat_1 = messageConcat_1 + "**Nome: **" + list_gamesNames[x - 1] + "\n**Link:** <" + list_gamesURL[x - 1] + ">" + \
                        "\n**Preço Original: **" + \
                        list_gamesOriginalPrice[x - 1] + "\n**Preço com Desconto: **" + \
                        list_gamesFinalPrice[x - 1] + "\n\n"
                else:
                    messageConcat_2 = messageConcat_2 + "**Nome: **" + list_gamesNames[x - 1] + "\n**Link:** <" + list_gamesURL[x - 1] + ">" + \
                        "\n**Preço Original: **" + \
                        list_gamesOriginalPrice[x - 1] + "\n**Preço com Desconto: **" + \
                        list_gamesFinalPrice[x - 1] + "\n\n"
                x = x - 1

            await message.channel.send(member.mention + messages.checkDm())
            await member.send(messageConcat_1)
            await member.send(messageConcat_2)
            await member.send("\n**{}**".format(messages.currencyAlert()))

    # Comando: $precompra ou $pc
    if(message.content.lower().startswith("$precompra") or message.content.lower().startswith("$pc")):
        list_gamesNames, list_gamesURL, list_gamesOriginalPrice, list_gamesFinalPrice = catchOffers.getTabContent(
            URL+'=ComingSoon', 'ComingSoonRows')
        list_gamesNames.reverse(), list_gamesURL.reverse(
        ), list_gamesOriginalPrice.reverse(), list_gamesFinalPrice.reverse()
        num = x = len(list_gamesNames)

        if(x == 0):
            await message.channel.send(messages.noOffers()[1])

        else:
            messageConcat_1 = ''
            messageConcat_2 = ''
            member = message.author
            while(x > 0):
                if(x >= num/2):
                    messageConcat_1 = messageConcat_1 + "**Nome: **" + list_gamesNames[x - 1] + "\n**Link:** <" + list_gamesURL[x - 1] + ">" + \
                        "\n**Preço Original: **" + \
                        list_gamesOriginalPrice[x - 1] + "\n**Preço com Desconto: **" + \
                        list_gamesFinalPrice[x - 1] + "\n\n"
                else:
                    messageConcat_2 = messageConcat_2 + "**Nome: **" + list_gamesNames[x - 1] + "\n**Link:** <" + list_gamesURL[x - 1] + ">" + \
                        "\n**Preço Original: **" + \
                        list_gamesOriginalPrice[x - 1] + "\n**Preço com Desconto: **" + \
                        list_gamesFinalPrice[x - 1] + "\n\n"
                x = x - 1

            await message.channel.send(member.mention + messages.checkDm())
            await member.send(messageConcat_1)
            await member.send(messageConcat_2)
            await member.send("\n**{}**".format(messages.currencyAlert()))

    # Comando: $game
    if(message.content.lower().startswith("$game")):
        gameName = message.content.split("$game ")

        if(len(gameName) == 1):
            await message.channel.send(messages.commandAlert()[0])
        else:
            gameName, gameURL, gameIMG, gamePrice, searchUrl = catchOffers.getSpecificGame(gameName[len(gameName) - 1])

            if(gameName != None):
                embedSpecificGame =  discord.Embed(
                    title="👾 Jogo: {} 👾".format(gameName),
                    color=COLOR
                )

                embedSpecificGame.set_image(url=gameIMG)
                embedSpecificGame.add_field(
                    name="**Link:**", value="**[Clique Aqui]({})**".format(gameURL), inline=False)

                if(len(gamePrice) > 1):
                    embedSpecificGame.add_field(
                        name="**Preço Original:**", value="**{}**".format(gamePrice[0]), inline=True)
                    embedSpecificGame.add_field(
                        name="**Preço com Desconto:**", value="**{}**".format(gamePrice[1]), inline=True)
                else:
                    embedSpecificGame.add_field(
                        name="**Preço:**", value="**{}**".format(gamePrice[0]), inline=False)

                if(gamePrice[0].find('Gratuito') == -1):
                    embedSpecificGame.set_footer(text=messages.currencyAlert())

                embedSpecificGame.add_field(
                    name="**Obs:**", value=messages.wrongGame(searchUrl), inline=False)

                await message.channel.send(embed=embedSpecificGame)
            
            else:
                await message.channel.send(messages.noOffers()[2])

# Mudar o Status do bot automaticamente e de forma aleatória.
async def changeStatus():
    await client.wait_until_ready()
    await asyncio.sleep(20)
    
    while not client.is_closed():
        numServers = len(client.guilds)
        msgStatus = messages.status(numServers)
        randomStatus = messages.randomMessage(msgStatus, len(msgStatus))
        game = discord.Game(randomStatus)
        online = discord.Status.online

        await client.change_presence(status=online, activity=game)
        await asyncio.sleep(20)


client.loop.create_task(changeStatus())

client.run(TOKEN)