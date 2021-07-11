import asyncio
import discord
from time import sleep

from myUtils.catch_offers import CatchOffers
from myUtils import messages
from myUtils import discordToken

COLOR = 0xa82fd2
INVITE = "https://discord.com/oauth2/authorize?client_id=714852360241020929&scope=bot&permissions=485440"
URL = "https://store.steampowered.com/specials?cc=br#p=0&tab="
TOKEN = discordToken.myToken()

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
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
    
    if(not message.author.bot):
        # Comando: $help ou $ajuda ou $comandos
        if(
            message.content.lower().startswith("$help") or 
            message.content.lower().startswith("$ajuda") or 
            message.content.lower().startswith("$comandos")
        ):
            help_ = message.content.split(" ")

            if(len(help_) != 2):
                embedHelp = discord.Embed(
                    color = COLOR
                )
                embedHelp.set_author(
                    name = "SteamOffersBot lista de comandos:", 
                    icon_url=client.user.avatar_url
                )
                embedHelp.add_field(
                    name="```$promocao``` ou ```$pr```",
                    value=messages.helpValues()[0], 
                    inline=False
                )
                embedHelp.add_field(
                    name="```$destaque``` ou ```$dt```",
                    value=messages.helpValues()[1], 
                    inline=False
                )
                embedHelp.add_field(
                    name="```$novidades``` ou ```$populares``` ou ```$np```",
                    value=messages.helpValues()[2], 
                    inline=False
                )
                embedHelp.add_field(
                    name="```$maisvendidos``` ou ```$mv```",
                    value=messages.helpValues()[3], 
                    inline=False
                )
                embedHelp.add_field(
                    name="```$jogospopulares``` ou ```$jp```",
                    value=messages.helpValues()[4], 
                    inline=False
                )
                embedHelp.add_field(
                    name="```$prevenda``` ou ```$pv```",
                    value=messages.helpValues()[5], 
                    inline=False
                )
                embedHelp.add_field(
                    name="```$convite```",
                    value=messages.helpValues()[6], 
                    inline=False
                )
                embedHelp.add_field(
                    name="```$botinfo```",
                    value=messages.helpValues()[7], 
                    inline=False
                )
                embedHelp.add_field(
                    name="```$game [nome do jogo]```",
                    value=messages.helpValues()[8], 
                    inline=False
                )
                embedHelp.add_field(
                    name="```$genre [gênero do jogo]```",
                    value=messages.helpValues()[9], 
                    inline=False
                )
                embedHelp.add_field(
                    name="```$maxprice [preço]```",
                    value=messages.helpValues()[10], 
                    inline=False
                )

                await message.channel.send(embed=embedHelp)
            else:
                # $help genre
                if(help_[1] == "genre"):
                    embedHelp = discord.Embed(
                        title = messages.title()[4],
                        color = COLOR,
                    )
                    embedHelp.add_field(
                        name=messages.emojisGameGenres()[0], 
                        value=messages.gameGenres()[0], 
                        inline=True
                    )
                    embedHelp.add_field(
                        name=messages.emojisGameGenres()[1], 
                        value=messages.gameGenres()[1], 
                        inline=True
                    )
                    embedHelp.add_field(
                        name=messages.emojisGameGenres()[2], 
                        value=messages.gameGenres()[2], 
                        inline=True
                    )
                    embedHelp.add_field(
                        name=messages.emojisGameGenres()[3], 
                        value=messages.gameGenres()[3], 
                        inline=False
                    )
                    embedHelp.add_field(
                        name=messages.emojisGameGenres()[4], 
                        value=messages.gameGenres()[4], 
                        inline=True
                    )
                    embedHelp.add_field(
                        name=messages.emojisGameGenres()[5], 
                        value=messages.gameGenres()[5], 
                        inline=True
                    )
                    embedHelp.add_field(
                        name=messages.emojisGameGenres()[6], 
                        value=messages.gameGenres()[6], 
                        inline=True
                    )
                    embedHelp.add_field(
                        name=messages.emojisGameGenres()[7], 
                        value=messages.gameGenres()[7], 
                        inline=False
                    )
                    embedHelp.add_field(
                        name=messages.emojisGameGenres()[8], 
                        value=messages.gameGenres()[8], 
                        inline=True
                    )
                    embedHelp.add_field(
                        name=messages.emojisGameGenres()[9], 
                        value=messages.gameGenres()[9], 
                        inline=True
                    )
                    embedHelp.set_footer(text="Utilize $genre [um dos gêneros acima]")

                    await message.channel.send(embed=embedHelp)
                else:
                    await message.channel.send(messages.commandAlert()[2])

        # Comando: $convite
        if(message.content.lower().startswith("$convite")):
            embedInvite = discord.Embed(
                title=messages.title()[0],
                color=COLOR,
                description='**{}**'.format(INVITE)
            )
            embedInvite.set_thumbnail(url=client.user.avatar_url)

            await message.channel.send(embed=embedInvite)

        # Comando: $destaque ou $dt
        if(
            message.content.lower().startswith("$destaque") or 
            message.content.lower().startswith("$dt")
        ):
            # Mensagem de busca, com efeito de carregamento.
            message_content = messages.searchMessage()[0]
            search_message = await message.channel.send(message_content)
            
            sleep(0.5)
            await search_message.edit(content=message_content+" **.**")
            
            sleep(0.5)
            await search_message.edit(content=message_content+" **. .**")

            list_gamesURl, list_gamesIMG, list_H2 = await catchOffers.getSpotlightOffers()
            x = len(list_gamesURl)

            if(x == 0):
                await search_message.edit(content=messages.noOffers()[0])
            else:
                first_iteration = True

                while(x > 0):
                    embedSpotlightGames = discord.Embed(
                        title=messages.title()[1],
                        color=COLOR
                    )
                    embedSpotlightGames.set_image(url=list_gamesIMG[x - 1])
                    embedSpotlightGames.add_field(
                        name="**Link:**", 
                        value="**[Clique Aqui]({})**".format(list_gamesURl[x - 1]), 
                        inline=False
                    )
                    embedSpotlightGames.add_field(
                        name="**Descrição:**", 
                        value="**{}**".format(list_H2[x - 1]), 
                        inline=False
                    )

                    if(first_iteration):
                        first_iteration = False
                        
                        await search_message.edit(content="", embed=embedSpotlightGames)
                    else:
                        await message.channel.send(embed=embedSpotlightGames)

                    x = x - 1

        # Comando: $promocao ou $pr
        if(
            message.content.lower().startswith("$promocao") or 
            (
                message.content.lower().startswith("$pr") and
                message.content == "$pr"
            )
        ):

            # Mensagem de busca, com efeito de carregamento.
            message_content = messages.searchMessage()[0]
            search_message = await message.channel.send(message_content)
            
            sleep(0.5)
            await search_message.edit(content=message_content+" **.**")
            
            sleep(0.5)
            await search_message.edit(content=message_content+" **. .**")

            list_gamesURl, list_gamesIMG = await catchOffers.getDailyGamesOffers()
            list_gamesOP, list_gamesFP = await catchOffers.getDailyGamesOffersPrices()
            x = len(list_gamesURl)

            if(x == 0):
                await search_message.edit(content=messages.noOffers()[1])
            else:
                first_iteration = True

                while(x > 0):
                    embedDailyGames = discord.Embed(
                        title=messages.title()[2],
                        color=COLOR
                    )
                    embedDailyGames.set_image(url=list_gamesIMG[x - 1])
                    embedDailyGames.add_field(
                        name="**Link:**", 
                        value="**[Clique Aqui]({})**".format(list_gamesURl[x - 1]), 
                        inline=False
                    )
                    embedDailyGames.add_field(
                        name="**Preço Original:**", 
                        value="**{}**".format(list_gamesOP[x - 1]), 
                        inline=True
                    )
                    embedDailyGames.add_field(
                        name="**Preço com Desconto:**", 
                        value="**{}**".format(list_gamesFP[x - 1]), 
                        inline=True
                    )

                    if(first_iteration):
                        first_iteration = False

                        await search_message.edit(content="", embed=embedDailyGames)
                    else:
                        await message.channel.send(embed=embedDailyGames)
                    
                    x = x - 1

        # Comando: $botinfo
        if(message.content.lower().startswith("$botinfo")):
            embedBotInfo = discord.Embed(
                title=messages.title()[3],
                color=COLOR
            )
            embedBotInfo.set_thumbnail(url=client.user.avatar_url)
            embedBotInfo.add_field(
                name="Python", 
                value=messages.infoValues()[0], 
                inline=True
            )
            embedBotInfo.add_field(
                name="discord.py", 
                value=messages.infoValues()[1], 
                inline=True
            )
            embedBotInfo.add_field(
                name="Sobre SteamOffersBot", 
                value=messages.infoValues()[2], 
                inline=False
            )
            embedBotInfo.set_author(
                name="ArticZ#1081", 
                icon_url=client.get_user(259443927441080330).avatar_url
            )
            embedBotInfo.set_footer(
                text="Criado em 26 de Maio de 2020! | Última atualização em {}."
                .format(messages.infoValues()[3])
            )

            await message.channel.send(embed=embedBotInfo)

        # Comando: $novidades ou $populares ou $np
        if(
            message.content.lower().startswith("$novidades") or 
            message.content.lower().startswith("$populares") or 
            message.content.lower().startswith("$np")
        ):
            (
                list_gamesNames, 
                list_gamesURL, 
                list_gamesOriginalPrice, 
                list_gamesFinalPrice, 
                list_gamesIMG
            ) = await catchOffers.getTabContent(URL+'=NewReleases', 'NewReleasesRows')
            
            list_gamesNames.reverse() 
            list_gamesURL.reverse() 
            list_gamesOriginalPrice.reverse() 
            list_gamesFinalPrice.reverse()
            
            num = x = len(list_gamesNames)

            if(x == 0):
                await message.channel.send(messages.noOffers()[1])

            else:
                messageConcat_1 = ''
                messageConcat_2 = ''
                member = message.author
                
                while(x > 0):
                    if(x >= (num/2)):
                        messageConcat_1 = messageConcat_1 + "**Nome: **" + \
                            list_gamesNames[x - 1] + "\n**Link:** <" + \
                            list_gamesURL[x - 1] + ">" + "\n**Preço Original: **" + \
                            list_gamesOriginalPrice[x - 1] + "\n**Preço com Desconto: **" + \
                            list_gamesFinalPrice[x - 1] + "\n\n"
                    else:
                        messageConcat_2 = messageConcat_2 + "**Nome: **" + \
                            list_gamesNames[x - 1] + "\n**Link:** <" + \
                            list_gamesURL[x - 1] + ">" + "\n**Preço Original: **" + \
                            list_gamesOriginalPrice[x - 1] + "\n**Preço com Desconto: **" + \
                            list_gamesFinalPrice[x - 1] + "\n\n"
                    
                    x = x - 1

                await message.channel.send(member.mention + messages.checkDm())
                await member.send(messageConcat_1)
                await member.send(messageConcat_2)

        # Comando: $maisvendidos ou $mv
        if(
            message.content.lower().startswith("$maisvendidos") or 
            message.content.lower().startswith("$mv")
        ):
            (
                list_gamesNames, 
                list_gamesURL, 
                list_gamesOriginalPrice, 
                list_gamesFinalPrice, 
                list_gamesIMG
            ) = await catchOffers.getTabContent(URL+'=TopSellers', 'TopSellersRows')
            
            list_gamesNames.reverse()
            list_gamesURL.reverse()
            list_gamesOriginalPrice.reverse()
            list_gamesFinalPrice.reverse()

            num = x = len(list_gamesNames)

            if(x == 0):
                await message.channel.send(messages.noOffers()[1])
            else:
                messageConcat_1 = ''
                messageConcat_2 = ''
                member = message.author
                
                while(x > 0):
                    if(x >= num/2):
                        messageConcat_1 = messageConcat_1 + "**Nome: **" + \
                            list_gamesNames[x - 1] + "\n**Link:** <" + \
                            list_gamesURL[x - 1] + ">" + "\n**Preço Original: **" + \
                            list_gamesOriginalPrice[x - 1] + "\n**Preço com Desconto: **" + \
                            list_gamesFinalPrice[x - 1] + "\n\n"
                    else:
                        messageConcat_2 = messageConcat_2 + "**Nome: **" + \
                            list_gamesNames[x - 1] + "\n**Link:** <" + \
                            list_gamesURL[x - 1] + ">" + "\n**Preço Original: **" + \
                            list_gamesOriginalPrice[x - 1] + "\n**Preço com Desconto: **" + \
                            list_gamesFinalPrice[x - 1] + "\n\n"
                    
                    x = x - 1

                await message.channel.send(member.mention + messages.checkDm())
                await member.send(messageConcat_1)
                await member.send(messageConcat_2)

        # Comando: $jogospopulares ou $jp
        if(
            message.content.lower().startswith("$jogospopulares") or 
            message.content.lower().startswith("$jp")
        ):
            (
                list_gamesNames, 
                list_gamesURL, 
                list_gamesOriginalPrice, 
                list_gamesFinalPrice, 
                list_gamesIMG
            ) = await catchOffers.getTabContent(URL+'=ConcurrentUsers', 'ConcurrentUsersRows')
            
            list_gamesNames.reverse()
            list_gamesURL.reverse()
            list_gamesOriginalPrice.reverse() 
            list_gamesFinalPrice.reverse()
            
            num = x = len(list_gamesNames)

            if(x == 0):
                await message.channel.send(messages.noOffers()[1])
            else:
                messageConcat_1 = ''
                messageConcat_2 = ''
                member = message.author
                
                while(x > 0):
                    if(x >= num/2):
                        messageConcat_1 = messageConcat_1 + "**Nome: **" + \
                            list_gamesNames[x - 1] + "\n**Link:** <" + \
                            list_gamesURL[x - 1] + ">" + "\n**Preço Original: **" + \
                            list_gamesOriginalPrice[x - 1] + "\n**Preço com Desconto: **" + \
                            list_gamesFinalPrice[x - 1] + "\n\n"
                    else:
                        messageConcat_2 = messageConcat_2 + "**Nome: **" + \
                            list_gamesNames[x - 1] + "\n**Link:** <" + \
                            list_gamesURL[x - 1] + ">" + "\n**Preço Original: **" + \
                            list_gamesOriginalPrice[x - 1] + "\n**Preço com Desconto: **" + \
                            list_gamesFinalPrice[x - 1] + "\n\n"
                    
                    x = x - 1

                await message.channel.send(member.mention + messages.checkDm())
                await member.send(messageConcat_1)
                await member.send(messageConcat_2)

        # Comando: $prevenda ou $pv
        if(
            message.content.lower().startswith("$prevenda") or 
            message.content.lower().startswith("$pv")
        ):
            (
                list_gamesNames, 
                list_gamesURL, 
                list_gamesOriginalPrice, 
                list_gamesFinalPrice, 
                list_gamesIMG
            ) = await catchOffers.getTabContent(URL+'=ComingSoon', 'ComingSoonRows')
            
            list_gamesNames.reverse()
            list_gamesURL.reverse()
            list_gamesOriginalPrice.reverse()
            list_gamesFinalPrice.reverse()
            
            num = x = len(list_gamesNames)

            if(x == 0):
                await message.channel.send(messages.noOffers()[1])
            else:
                messageConcat_1 = ''
                messageConcat_2 = ''
                member = message.author
                
                while(x > 0):
                    if(x >= num/2):
                        messageConcat_1 = messageConcat_1 + "**Nome: **" + \
                            list_gamesNames[x - 1] + "\n**Link:** <" + \
                            list_gamesURL[x - 1] + ">" + "\n**Preço Original: **" + \
                            list_gamesOriginalPrice[x - 1] + "\n**Preço com Desconto: **" + \
                            list_gamesFinalPrice[x - 1] + "\n\n"
                    else:
                        messageConcat_2 = messageConcat_2 + "**Nome: **" + \
                            list_gamesNames[x - 1] + "\n**Link:** <" + \
                            list_gamesURL[x - 1] + ">" + "\n**Preço Original: **" + \
                            list_gamesOriginalPrice[x - 1] + "\n**Preço com Desconto: **" + \
                            list_gamesFinalPrice[x - 1] + "\n\n"
                    
                    x = x - 1

                await message.channel.send(member.mention + messages.checkDm())
                await member.send(messageConcat_1)
                await member.send(messageConcat_2)

        # Comando: $game
        if(message.content.lower().startswith("$game")):
            game_name_message = message.content.split("$game ")

            if(len(game_name_message) == 1):
                await message.channel.send(messages.commandAlert()[0])
            else:
                game_name = game_name_message[1]
                
                # Mensagem de busca de jogo, com efeito de carregamento.
                message_content = messages.searchMessage()[1]
                search_game_message = await message.channel.send(message_content + " __"+ game_name + "__ .**")
                
                sleep(0.5)
                await search_game_message.edit(content=message_content + " __" + game_name + "__ . .**")
                
                sleep(0.5)
                await search_game_message.edit(content=message_content + " __"+ game_name + "__ . . .**")

                (
                    gameName, 
                    gameURL, 
                    gameIMG, 
                    gamePrice, 
                    searchUrl
                ) = await catchOffers.getSpecificGame(game_name)

                if(gameName != None):
                    embedSpecificGame =  discord.Embed(
                        title="👾 Jogo: {} 👾".format(gameName),
                        color=COLOR
                    )
                    embedSpecificGame.set_image(url=gameIMG)
                    embedSpecificGame.add_field(
                        name="**Link:**", 
                        value="**[Clique Aqui]({})**".format(gameURL), 
                        inline=False
                    )

                    if(len(gamePrice) > 1): # Caso o jogo esteja em promoção.
                        embedSpecificGame.add_field(
                            name="**Preço Original:**", 
                            value="**{}**".format(gamePrice[0]), 
                            inline=True
                        )
                        embedSpecificGame.add_field(
                            name="**Preço com Desconto:**", 
                            value="**{}**".format(gamePrice[1]), 
                            inline=True
                        )
                    else: # Caso o jogo não esteja em promoção.
                        embedSpecificGame.add_field(
                            name="**Preço:**", 
                            value="**{}**".format(gamePrice[0]), 
                            inline=False
                        )

                    embedSpecificGame.add_field(
                        name="**Obs:**", 
                        value=messages.wrongGame(searchUrl), 
                        inline=False
                    )

                    await search_game_message.edit(content="", embed=embedSpecificGame)
                else:
                    await search_game_message.edit(content=messages.noOffers()[2])

        # Comando: $genre
        if(message.content.lower().startswith("$genre")):
            game_genre_message = message.content.split("$genre ")

            if(len(game_genre_message) == 1):
                await message.channel.send(messages.commandAlert()[1])
            else:
                game_genre = game_genre_message[1]

                # Mensagem de busca, com efeito de carregamento.
                message_content = messages.searchMessage()[2]
                search_genre_message = await message.channel.send(message_content + " __"+ game_genre +"__ .**")
                
                sleep(0.5)
                await search_genre_message.edit(content=message_content + " __" + game_genre + "__ . .**")
                
                sleep(0.5)
                await search_genre_message.edit(content=message_content + " __" + game_genre + "__ . . .**")

                (
                    gameName, 
                    gameURL, 
                    gameOriginalPrice , 
                    gameFinalPrice, 
                    gameIMG
                ) = await catchOffers.getGameRecommendationByGenre(game_genre)

                if(gameName != None):
                    embedGameRecommendationByGenre = discord.Embed(
                        title = messages.title(genre=game_genre)[5],
                        color = COLOR
                    )
                    embedGameRecommendationByGenre.set_image(url=gameIMG)
                    embedGameRecommendationByGenre.add_field(
                        name="**Nome:**", 
                        value="**{}**".format(gameName), 
                        inline=False
                    )
                    embedGameRecommendationByGenre.add_field(
                        name="**Link:**", 
                        value="**[Clique Aqui]({})**".format(gameURL), 
                        inline=False
                    )

                    if(
                        (gameOriginalPrice == gameFinalPrice) and 
                        (gameOriginalPrice != "Gratuiro p/ Jogar")
                    ):
                        embedGameRecommendationByGenre.add_field(
                            name="**Preço:**", 
                            value="**{}**".format(gameOriginalPrice), 
                            inline=True
                        )
                    else:
                        if(gameOriginalPrice != "Gratuiro p/ Jogar"):
                            embedGameRecommendationByGenre.add_field(
                                name="**Preço Original:**", 
                                value="**{}**".format(gameOriginalPrice), 
                                inline=True
                            )
                            embedGameRecommendationByGenre.add_field(
                                name="**Preço com Desconto:**", 
                                value="**{}**".format(gameFinalPrice), 
                                inline=True
                            )
                        else:
                            embedGameRecommendationByGenre.add_field(
                                name="**Preço:**", 
                                value="**{}**".format(gameOriginalPrice), 
                                inline=True
                            )

                    await search_genre_message.edit(content="", embed=embedGameRecommendationByGenre)
                else:
                    await search_genre_message.edit(content=messages.noOffers()[3])

        if(
            message.content.lower().startswith("$maxprice")
        ):
            max_price_message = message.content.split("$maxprice ")
            max_price = max_price_message[1]
            
            if(max_price_message[1].isnumeric()):
                # Mensagem de busca de jogo, com efeito de carregamento.
                message_content = messages.searchMessage()[3]
                search_game_message = await message.channel.send(message_content + " "+ max_price + "__ .**")
                
                sleep(0.5)
                await search_game_message.edit(content=message_content + " " + max_price + "__ . .**")
                
                sleep(0.5)
                await search_game_message.edit(content=message_content + " "+ max_price + "__ . . .**")

                if(int(max_price_message[1]) > 120):
                    max_price = "rZ04j"
                elif(int(max_price_message[1]) < 10):
                    max_price = "19Jfc"
                
                (
                    gameName,
                    gameIMG, 
                    gameURL, 
                    gamePrice
                    
                ) = await catchOffers.getGameRecommendationByPriceRange(max_price)

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
                
                if(gamePrice[0] != gamePrice[1]): # Caso o jogo esteja em promoção.
                    embedGameRecommendationByPrice.add_field(
                        name="**Preço Original:**", 
                        value="**{}**".format(gamePrice[0]), 
                        inline=True
                    )
                    embedGameRecommendationByPrice.add_field(
                        name="**Preço com Desconto:**", 
                        value="**{}**".format(gamePrice[1]), 
                        inline=True
                    )
                else: # Caso o jogo não esteja em promoção.
                    embedGameRecommendationByPrice.add_field(
                        name="**Preço:**", 
                        value="**{}**".format(gamePrice[0]), 
                        inline=False
                    )

                if(int(max_price_message[1]) > 120):
                    embedGameRecommendationByPrice.set_footer(
                        text=messages.recommendationByPrice()[1]
                    )
                elif(int(max_price_message[1]) < 10):
                    embedGameRecommendationByPrice.set_footer(
                        text=messages.recommendationByPrice()[2]
                    )
                
                await search_game_message.edit(content="", embed=embedGameRecommendationByPrice)
            else:
                await message.channel.send(messages.recommendationByPrice()[0])


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