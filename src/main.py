import asyncio
import discord
from time import sleep

from services.catchOffers import CatchOffers
from services import messages
from services import discordToken

# ------------------------------ Constants ----------------------------------- #
PREFIX = "$"
COLOR = 0xa82fd2
INVITE = "https://discord.com/oauth2/authorize?client_id=714852360241020929&scope=bot&permissions=485440"
URL = "https://store.steampowered.com/specials?cc=br#p=0&tab="
TOKEN = discordToken.myToken()
# ---------------------------------------------------------------------------- #

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
catchOffers = CatchOffers()

@client.event
async def on_ready():
    numServers = len(client.guilds)

    print("\n{} está online em {} servidores".format(client.user.name, numServers))

    game   = discord.Game("Online em {} Servidores".format(numServers))
    online = discord.Status.online

    await client.change_presence(status=online, activity=game)

@client.event
async def on_message(message):
    
    if(not message.author.bot):
        # Comando: $help ou $ajuda ou $comandos
        if(
            message.content.lower().startswith(PREFIX + "help") or 
            message.content.lower().startswith(PREFIX + "ajuda") or 
            message.content.lower().startswith(PREFIX + "comandos")
        ):
            __help__ = message.content.split(" ")

            if(len(__help__) != 2):
                embedHelp = discord.Embed(
                    color = COLOR
                )
                embedHelp.set_author(
                    name     = "SteamOffersBot lista de comandos:", 
                    icon_url = client.user.avatar_url
                )
                embedHelp.add_field(
                    name   = "```{}promocao``` ou ```{}pr```".format(PREFIX, PREFIX),
                    value  = messages.helpValues()[0], 
                    inline = False
                )
                embedHelp.add_field(
                    name   = "```{}destaque``` ou ```{}dt```".format(PREFIX, PREFIX),
                    value  = messages.helpValues()[1], 
                    inline = False
                )
                embedHelp.add_field(
                    name   = "```{}novidades``` ou ```{}populares``` ou ```{}np```".format(PREFIX, PREFIX, PREFIX),
                    value  = messages.helpValues()[2], 
                    inline = False
                )
                embedHelp.add_field(
                    name   = "```{}maisvendidos``` ou ```{}mv```".format(PREFIX, PREFIX),
                    value  = messages.helpValues()[3], 
                    inline = False
                )
                embedHelp.add_field(
                    name   = "```{}jogospopulares``` ou ```{}jp```".format(PREFIX, PREFIX),
                    value  = messages.helpValues()[4], 
                    inline = False
                )
                embedHelp.add_field(
                    name   = "```{}prevenda``` ou ```{}pv```".format(PREFIX, PREFIX),
                    value  = messages.helpValues()[5], 
                    inline = False
                )
                embedHelp.add_field(
                    name   = "```{}convite```".format(PREFIX),
                    value  = messages.helpValues()[6], 
                    inline = False
                )
                embedHelp.add_field(
                    name   = "```{}botinfo```".format(PREFIX),
                    value  = messages.helpValues()[7], 
                    inline = False
                )
                embedHelp.add_field(
                    name   = "```{}game [nome do jogo]```".format(PREFIX),
                    value  = messages.helpValues()[8], 
                    inline = False
                )
                embedHelp.add_field(
                    name   = "```{}genre [gênero do jogo]```".format(PREFIX),
                    value  = messages.helpValues()[9], 
                    inline = False
                )
                embedHelp.add_field(
                    name   = "```{}maxprice [preço]```".format(PREFIX),
                    value  = messages.helpValues()[10], 
                    inline = False
                )

                await message.channel.send(embed=embedHelp)
            else:
                # $help genre
                if(__help__[1] == "genre"):
                    embedHelp = discord.Embed(
                        title = messages.title()[4],
                        color = COLOR,
                        description = messages.gameGenres()
                    )
                    embedHelp.add_field(
                        name   = "Ficou confuso(a) ?",
                        value  = messages.helpValues()[11],
                        inline = False
                    )
                    embedHelp.set_footer(text="Utilize {}genre [um dos gêneros acima]".format(PREFIX))

                    await message.channel.send(embed=embedHelp)
                else:
                    await message.channel.send(messages.commandAlert()[2])

        # Comando: $invite ou $convite
        if(
            message.content.lower().startswith(PREFIX + "invite") or
            message.content.lower().startswith(PREFIX + "convite")
        ):
            embedInvite = discord.Embed(
                title       = messages.title()[0],
                color       = COLOR,
                description = '**{}**'.format(INVITE)
            )
            embedInvite.set_thumbnail(url=client.user.avatar_url)

            await message.channel.send(embed=embedInvite)

        # Comando: $destaque ou $dt
        if(
            message.content.lower().startswith(PREFIX + "destaque") or 
            message.content.lower().startswith(PREFIX + "dt")
        ):
            # Mensagem de busca, com efeito de carregamento.
            messageContent = messages.searchMessage()[0]
            searchMessage  = await message.channel.send(messageContent)
            
            sleep(0.5)
            await searchMessage.edit(content=messageContent+" **.**")
            
            sleep(0.5)
            await searchMessage.edit(content=messageContent+" **. .**")

            (
                gamesUrls, 
                gamesImages, 
                gamesContents
            ) = await catchOffers.getSpotlightOffers()
            x = len(gamesUrls)

            if(x == 0):
                await searchMessage.edit(content=messages.noOffers()[0])
            else:
                first_iteration = True

                while(x > 0):
                    embedSpotlightGames = discord.Embed(
                        title = messages.title()[1],
                        color = COLOR
                    )
                    embedSpotlightGames.set_image(url=gamesImages[x - 1])
                    embedSpotlightGames.add_field(
                        name   = "**Link:**", 
                        value  = "**[Clique Aqui]({})**".format(gamesUrls[x - 1]["value"]), 
                        inline = False
                    )
                    embedSpotlightGames.add_field(
                        name   = "**Descrição:**", 
                        value  = "**{}**".format(gamesContents[x - 1]["value"]), 
                        inline = False
                    )

                    if(first_iteration):
                        first_iteration = False
                        
                        await searchMessage.edit(content="", embed=embedSpotlightGames)
                    else:
                        await message.channel.send(embed=embedSpotlightGames)

                    x = x - 1

        # Comando: $promocao ou $pr
        if(
            message.content.lower().startswith(PREFIX + "promocao") or 
            message.content.lower().startswith(PREFIX + "promoção") or 
            (
                message.content.lower().startswith(PREFIX + "pr") and
                message.content == PREFIX + "pr"
            )
        ):

            # Mensagem de busca, com efeito de carregamento.
            messageContent = messages.searchMessage()[0]
            searchMessage  = await message.channel.send(messageContent)
            
            sleep(0.5)
            await searchMessage.edit(content=messageContent+" **.**")
            
            sleep(0.5)
            await searchMessage.edit(content=messageContent+" **. .**")

            (
                gamesUrls, 
                gamesImages,
                gamesOriginalPrices,
                gamesFinalPrices
            ) = await catchOffers.getDailyGamesOffers()
            x = len(gamesUrls)

            if(x == 0):
                await searchMessage.edit(content=messages.noOffers()[1])
            else:
                first_iteration = True

                while(x > 0):
                    embedDailyGames = discord.Embed(
                        title = messages.title()[2],
                        color = COLOR
                    )
                    embedDailyGames.set_image(url=gamesImages[x - 1])
                    embedDailyGames.add_field(
                        name   = "**Link:**", 
                        value  = "**[Clique Aqui]({})**".format(gamesUrls[x - 1]), 
                        inline = False
                    )
                    embedDailyGames.add_field(
                        name   = "**Preço Original:**", 
                        value  = "**{}**".format(gamesOriginalPrices[x - 1]), 
                        inline = True
                    )
                    embedDailyGames.add_field(
                        name   = "**Preço com Desconto:**", 
                        value  = "**{}**".format(gamesFinalPrices[x - 1]), 
                        inline = True
                    )

                    if(first_iteration):
                        first_iteration = False

                        await searchMessage.edit(content="", embed=embedDailyGames)
                    else:
                        await message.channel.send(embed=embedDailyGames)
                    
                    x = x - 1

        # Comando: $botinfo
        if(
            message.content.lower().startswith(PREFIX + "botinfo") or
            message.content.lower().startswith(PREFIX + "info")
        ):
            embedBotInfo = discord.Embed(
                title = messages.title()[3],
                color = COLOR
            )
            embedBotInfo.set_thumbnail(url=client.user.avatar_url)
            embedBotInfo.add_field(
                name   = "Python", 
                value  = messages.infoValues()[0], 
                inline = True
            )
            embedBotInfo.add_field(
                name   = "discord.py", 
                value  = messages.infoValues()[1], 
                inline = True
            )
            embedBotInfo.add_field(
                name   = "Sobre SteamOffersBot", 
                value  = messages.infoValues()[2], 
                inline = False
            )
            embedBotInfo.set_author(
                name     = "ArticZ#1081", 
                icon_url = client.get_user(259443927441080330).avatar_url
            )
            embedBotInfo.set_footer(
                text="Criado em 26 de Maio de 2020! | Última atualização em {}."
                .format(messages.infoValues()[3])
            )

            await message.channel.send(embed=embedBotInfo)

        # Comando: $novidades ou $populares ou $np
        if(
            message.content.lower().startswith(PREFIX + "novidades") or 
            message.content.lower().startswith(PREFIX + "populares") or 
            message.content.lower().startswith(PREFIX + "np")
        ):
            (
                gamesNames, 
                gamesUrls, 
                gamesOriginalPrices, 
                gamesFinalPrices, 
                gamesImages
            ) = await catchOffers.getTabContent(URL+'=NewReleases', 'NewReleasesRows')
            
            gamesNames.reverse() 
            gamesUrls.reverse() 
            gamesOriginalPrices.reverse() 
            gamesFinalPrices.reverse()
            
            num = x = len(gamesNames)

            if(x == 0):
                await message.channel.send(messages.noOffers()[1])
            else:
                messageConcat0 = ''
                messageConcat1 = ''
                member          = message.author
                
                while(x > 0):
                    if(x >= (num/2)):
                        messageConcat0 = messageConcat0 + "**Nome: **" + \
                            gamesNames[x - 1] + "\n**Link:** <" + \
                            gamesUrls[x - 1] + ">" + "\n**Preço Original: **" + \
                            gamesOriginalPrices[x - 1] + "\n**Preço com Desconto: **" + \
                            gamesFinalPrices[x - 1] + "\n\n"
                    else:
                        messageConcat1 = messageConcat1 + "**Nome: **" + \
                            gamesNames[x - 1] + "\n**Link:** <" + \
                            gamesUrls[x - 1] + ">" + "\n**Preço Original: **" + \
                            gamesOriginalPrices[x - 1] + "\n**Preço com Desconto: **" + \
                            gamesFinalPrices[x - 1] + "\n\n"
                    
                    x = x - 1

                await message.channel.send(member.mention + messages.checkDm())
                await member.send(messageConcat0)
                await member.send(messageConcat1)

        # Comando: $maisvendidos ou $mv
        if(
            message.content.lower().startswith(PREFIX + "maisvendidos") or 
            message.content.lower().startswith(PREFIX + "mv")
        ):
            (
                gamesNames, 
                gamesUrls, 
                gamesOriginalPrices, 
                gamesFinalPrices, 
                gamesImages
            ) = await catchOffers.getTabContent(URL+'=TopSellers', 'TopSellersRows')
            
            gamesNames.reverse()
            gamesUrls.reverse()
            gamesOriginalPrices.reverse()
            gamesFinalPrices.reverse()

            num = x = len(gamesNames)

            if(x == 0):
                await message.channel.send(messages.noOffers()[1])
            else:
                messageConcat0 = ''
                messageConcat1 = ''
                member          = message.author
                
                while(x > 0):
                    if(x >= num/2):
                        messageConcat0 = messageConcat0 + "**Nome: **" + \
                            gamesNames[x - 1] + "\n**Link:** <" + \
                            gamesUrls[x - 1] + ">" + "\n**Preço Original: **" + \
                            gamesOriginalPrices[x - 1] + "\n**Preço com Desconto: **" + \
                            gamesFinalPrices[x - 1] + "\n\n"
                    else:
                        messageConcat1 = messageConcat1 + "**Nome: **" + \
                            gamesNames[x - 1] + "\n**Link:** <" + \
                            gamesUrls[x - 1] + ">" + "\n**Preço Original: **" + \
                            gamesOriginalPrices[x - 1] + "\n**Preço com Desconto: **" + \
                            gamesFinalPrices[x - 1] + "\n\n"
                    
                    x = x - 1

                await message.channel.send(member.mention + messages.checkDm())
                await member.send(messageConcat0)
                await member.send(messageConcat1)

        # Comando: $jogospopulares ou $jp
        if(
            message.content.lower().startswith(PREFIX + "jogospopulares") or 
            message.content.lower().startswith(PREFIX + "jp")
        ):
            (
                gamesNames, 
                gamesUrls, 
                gamesOriginalPrices, 
                gamesFinalPrices, 
                gamesImages
            ) = await catchOffers.getTabContent(URL+'=ConcurrentUsers', 'ConcurrentUsersRows')
            
            gamesNames.reverse()
            gamesUrls.reverse()
            gamesOriginalPrices.reverse() 
            gamesFinalPrices.reverse()
            
            num = x = len(gamesNames)

            if(x == 0):
                await message.channel.send(messages.noOffers()[1])
            else:
                messageConcat0 = ''
                messageConcat1 = ''
                member          = message.author
                
                while(x > 0):
                    if(x >= num/2):
                        messageConcat0 = messageConcat0 + "**Nome: **" + \
                            gamesNames[x - 1] + "\n**Link:** <" + \
                            gamesUrls[x - 1] + ">" + "\n**Preço Original: **" + \
                            gamesOriginalPrices[x - 1] + "\n**Preço com Desconto: **" + \
                            gamesFinalPrices[x - 1] + "\n\n"
                    else:
                        messageConcat1 = messageConcat1 + "**Nome: **" + \
                            gamesNames[x - 1] + "\n**Link:** <" + \
                            gamesUrls[x - 1] + ">" + "\n**Preço Original: **" + \
                            gamesOriginalPrices[x - 1] + "\n**Preço com Desconto: **" + \
                            gamesFinalPrices[x - 1] + "\n\n"
                    
                    x = x - 1

                await message.channel.send(member.mention + messages.checkDm())
                await member.send(messageConcat0)
                await member.send(messageConcat1)

        # Comando: $prevenda ou $pv
        if(
            message.content.lower().startswith(PREFIX + "prevenda") or 
            message.content.lower().startswith(PREFIX + "pv")
        ):
            (
                gamesNames, 
                gamesUrls, 
                gamesOriginalPrices, 
                gamesFinalPrices, 
                gamesImages
            ) = await catchOffers.getTabContent(URL+'=ComingSoon', 'ComingSoonRows')
            
            gamesNames.reverse()
            gamesUrls.reverse()
            gamesOriginalPrices.reverse()
            gamesFinalPrices.reverse()
            
            num = x = len(gamesNames)

            if(x == 0):
                await message.channel.send(messages.noOffers()[1])
            else:
                messageConcat0 = ''
                messageConcat1 = ''
                member          = message.author
                
                while(x > 0):
                    if(x >= num/2):
                        messageConcat0 = messageConcat0 + "**Nome: **" + \
                            gamesNames[x - 1] + "\n**Link:** <" + \
                            gamesUrls[x - 1] + ">" + "\n**Preço Original: **" + \
                            gamesOriginalPrices[x - 1] + "\n**Preço com Desconto: **" + \
                            gamesFinalPrices[x - 1] + "\n\n"
                    else:
                        messageConcat1 = messageConcat1 + "**Nome: **" + \
                            gamesNames[x - 1] + "\n**Link:** <" + \
                            gamesUrls[x - 1] + ">" + "\n**Preço Original: **" + \
                            gamesOriginalPrices[x - 1] + "\n**Preço com Desconto: **" + \
                            gamesFinalPrices[x - 1] + "\n\n"
                    
                    x = x - 1

                await message.channel.send(member.mention + messages.checkDm())
                await member.send(messageConcat0)
                await member.send(messageConcat1)

        # Comando: $game
        if(message.content.lower().startswith(PREFIX + "game")):
            gameNameMessage = message.content.split(PREFIX + "game ")

            if(len(gameNameMessage) == 1):
                await message.channel.send(messages.commandAlert()[0])
            else:
                gameNameToSearch = gameNameMessage[1]
                
                # Mensagem de busca de jogo, com efeito de carregamento.
                messageContent     = messages.searchMessage()[1]
                searchGameMessage = await message.channel.send(messageContent + " __"+ gameNameToSearch + "__ .**")
                
                sleep(0.5)
                await searchGameMessage.edit(content=messageContent + " __" + gameNameToSearch + "__ . .**")
                
                sleep(0.5)
                await searchGameMessage.edit(content=messageContent + " __"+ gameNameToSearch + "__ . . .**")

                (
                    gameName, 
                    gameURL, 
                    gameIMG, 
                    gameOriginalPrice,
                    gameFinalPrice,
                    searchUrl
                ) = await catchOffers.getSpecificGame(gameNameToSearch)

                if(gameName != None):
                    embedSpecificGame =  discord.Embed(
                        title = "👾 Jogo: {} 👾".format(gameName),
                        color = COLOR
                    )
                    embedSpecificGame.set_image(url=gameIMG)
                    embedSpecificGame.add_field(
                        name   = "**Link:**", 
                        value  = "**[Clique Aqui]({})**".format(gameURL), 
                        inline = False
                    )

                    if(gameOriginalPrice != gameFinalPrice): # Caso o jogo esteja em promoção.
                        embedSpecificGame.add_field(
                            name   = "**Preço Original:**", 
                            value  = "**{}**".format(gameOriginalPrice), 
                            inline = True
                        )
                        embedSpecificGame.add_field(
                            name   = "**Preço com Desconto:**", 
                            value  = "**{}**".format(gameFinalPrice), 
                            inline = True
                        )
                    else: # Caso o jogo não esteja em promoção.
                        embedSpecificGame.add_field(
                            name   = "**Preço:**", 
                            value  = "**{}**".format(gameOriginalPrice), 
                            inline = False
                        )

                    embedSpecificGame.add_field(
                        name   = "**Obs:**", 
                        value  = messages.wrongGame(searchUrl), 
                        inline = False
                    )

                    await searchGameMessage.edit(content="", embed=embedSpecificGame)
                else:
                    await searchGameMessage.edit(content=messages.noOffers()[2])

        # Comando: $genre
        if(message.content.lower().startswith(PREFIX + "genre")):
            gameGenreMessage = message.content.split(PREFIX + "genre ")

            if(len(gameGenreMessage) == 1):
                await message.channel.send(messages.commandAlert()[1])
            else:
                gameGenreToSearch = gameGenreMessage[1]

                # Mensagem de busca, com efeito de carregamento.
                messageContent      = messages.searchMessage()[2]
                searchGenreMessage = await message.channel.send(messageContent + " __"+ gameGenreToSearch +"__ .**")
                
                sleep(0.5)
                await searchGenreMessage.edit(content=messageContent + " __" + gameGenreToSearch + "__ . .**")
                
                sleep(0.5)
                await searchGenreMessage.edit(content=messageContent + " __" + gameGenreToSearch + "__ . . .**")

                (
                    gameName, 
                    gameURL, 
                    gameOriginalPrice , 
                    gameFinalPrice, 
                    gameIMG
                ) = await catchOffers.getGameRecommendationByGenre(gameGenreToSearch)

                if(gameName != None):
                    embedGameRecommendationByGenre = discord.Embed(
                        title = messages.title(genre=gameGenreToSearch)[5],
                        color = COLOR
                    )
                    embedGameRecommendationByGenre.set_image(url=gameIMG)
                    embedGameRecommendationByGenre.add_field(
                        name   = "**Nome:**", 
                        value  = "**{}**".format(gameName), 
                        inline = False
                    )
                    embedGameRecommendationByGenre.add_field(
                        name   = "**Link:**", 
                        value  = "**[Clique Aqui]({})**".format(gameURL), 
                        inline = False
                    )

                    if(
                        (gameOriginalPrice == gameFinalPrice) and 
                        (gameOriginalPrice != "Gratuiro p/ Jogar")
                    ):
                        embedGameRecommendationByGenre.add_field(
                            name   = "**Preço:**", 
                            value  = "**{}**".format(gameOriginalPrice), 
                            inline = True
                        )
                    else:
                        if(gameOriginalPrice != "Gratuiro p/ Jogar"):
                            embedGameRecommendationByGenre.add_field(
                                name   = "**Preço Original:**", 
                                value  = "**{}**".format(gameOriginalPrice), 
                                inline = True
                            )
                            embedGameRecommendationByGenre.add_field(
                                name   = "**Preço com Desconto:**", 
                                value  = "**{}**".format(gameFinalPrice), 
                                inline = True
                            )
                        else:
                            embedGameRecommendationByGenre.add_field(
                                name   = "**Preço:**", 
                                value  = "**{}**".format(gameOriginalPrice), 
                                inline = True
                            )

                    await searchGenreMessage.edit(content="", embed=embedGameRecommendationByGenre)
                else:
                    await searchGenreMessage.edit(content=messages.noOffers()[3])

        if(
            message.content.lower().startswith(PREFIX + "maxprice")
        ):
            maxPriceMessage = message.content.split(PREFIX + "maxprice ")
            maxPrice         = maxPriceMessage[1]
            
            if(maxPriceMessage[1].isnumeric()):
                # Mensagem de busca de jogo, com efeito de carregamento.
                messageContent = messages.searchMessage()[3]
                searchGameMessage = await message.channel.send(messageContent + " "+ maxPrice + "__ .**")
                
                sleep(0.5)
                await searchGameMessage.edit(content=messageContent + " " + maxPrice + "__ . .**")
                
                sleep(0.5)
                await searchGameMessage.edit(content=messageContent + " "+ maxPrice + "__ . . .**")

                if(int(maxPriceMessage[1]) > 120):
                    maxPrice = "rZ04j"
                elif(int(maxPriceMessage[1]) < 10):
                    maxPrice = "19Jfc"
                
                (
                    gameName,
                    gameIMG, 
                    gameURL, 
                    gameOriginalPrice,
                    gameFinalPrice
                    
                ) = await catchOffers.getGameRecommendationByPriceRange(maxPrice)

                embedGameRecommendationByPrice = discord.Embed(
                    title = messages.title(gameName=gameName)[6],
                    color = COLOR
                )
                embedGameRecommendationByPrice.set_image(url=gameIMG)
                embedGameRecommendationByPrice.add_field(
                    name="**Link:**", 
                    value="**[Clique Aqui]({})**".format(gameURL), 
                    inline=False
                )
                
                if(gameOriginalPrice != gameFinalPrice): # Caso o jogo esteja em promoção.
                    embedGameRecommendationByPrice.add_field(
                        name="**Preço Original:**", 
                        value="**{}**".format(gameOriginalPrice), 
                        inline=True
                    )
                    embedGameRecommendationByPrice.add_field(
                        name="**Preço com Desconto:**", 
                        value="**{}**".format(gameFinalPrice), 
                        inline=True
                    )
                else: # Caso o jogo não esteja em promoção.
                    embedGameRecommendationByPrice.add_field(
                        name="**Preço:**", 
                        value="**{}**".format(gameOriginalPrice), 
                        inline=False
                    )

                if(int(maxPriceMessage[1]) > 120):
                    embedGameRecommendationByPrice.set_footer(
                        text=messages.recommendationByPrice()[1]
                    )
                elif(int(maxPriceMessage[1]) < 10):
                    embedGameRecommendationByPrice.set_footer(
                        text=messages.recommendationByPrice()[2]
                    )
                
                await searchGameMessage.edit(content="", embed=embedGameRecommendationByPrice)
            else:
                await message.channel.send(messages.recommendationByPrice()[0])


# Mudar o Status do bot automaticamente e de forma aleatória.
async def changeStatus():
    await client.wait_until_ready()
    await asyncio.sleep(20)
    
    while not client.is_closed():
        numServers = len(client.guilds)
        msgStatus = messages.status(PREFIX, numServers)
        randomStatus = messages.randomMessage(msgStatus)
        game = discord.Game(randomStatus)
        online = discord.Status.online

        await client.change_presence(status=online, activity=game)
        await asyncio.sleep(20)

client.loop.create_task(changeStatus())

client.run(TOKEN)