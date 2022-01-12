import os
import asyncio
import discord
from time import sleep
from re import search
from dotenv import load_dotenv

from services.crawler import Crawler
from services import messages

from services.GameReview.gameReviewEmbed import gameReviewEmbed
from services.SpecificGame.specificGameEmbed import specificGameEmbed

load_dotenv()

# ------------------------------ Constants ----------------------------------- #
PREFIX          = os.getenv("PREFIX")
COLOR           = 0xa82fd2
INVITE          = "https://discord.com/oauth2/authorize?client_id=714852360241020929&scope=bot&permissions=485440"
URL             = "https://store.steampowered.com/specials?cc=br#p=0&tab="
IMG_GENRES      = "https://i.imgur.com/q0NfeWX.png"
TOKEN           = os.getenv("DISCORD_TOKEN")
AUTHOR_ID       = int(os.getenv("AUTHOR_ID"))
REACTION_REVIEW = "👍"
REACTION_GAME   = "🎮"
# ---------------------------------------------------------------------------- #

intents           = discord.Intents.default()
intents.members   = True
intents.reactions = True

client  = discord.Client(intents=intents)
crawler = Crawler()

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
        if(message.content.lower().startswith(PREFIX)):
            __command__ = message.content.lower().split(PREFIX)[1]
            
            # Comando: $help ou $ajuda ou $comandos
            if(
                __command__.find("help")     == 0 or
                __command__.find("ajuda")    == 0 or
                __command__.find("comandos") == 0
            ):
                __help__ = __command__.split(" ")

                if(len(__help__) != 2):
                    embedHelp = discord.Embed(
                        color = COLOR
                    )
                    embedHelp.set_author(
                        name     = "SteamOffersBot lista de comandos:", 
                        icon_url = client.user.avatar_url
                    )
                    embedHelp.add_field(
                        name   = "```{0}promoção``` ou ```{0}pr```".format(PREFIX),
                        value  = messages.helpValues()[1], 
                        inline = False
                    )
                    embedHelp.add_field(
                        name   = "```{0}destaque``` ou ```{0}dt```".format(PREFIX),
                        value  = messages.helpValues()[2], 
                        inline = False
                    )
                    embedHelp.add_field(
                        name   = "```{0}novidades``` ou ```{0}populares``` ou ```{0}np```".format(PREFIX),
                        value  = messages.helpValues()[3], 
                        inline = False
                    )
                    embedHelp.add_field(
                        name   = "```{0}mais vendidos``` ou ```{0}mv```".format(PREFIX),
                        value  = messages.helpValues()[4], 
                        inline = False
                    )
                    embedHelp.add_field(
                        name   = "```{0}jogos populares``` ou ```{0}jp```".format(PREFIX),
                        value  = messages.helpValues()[5], 
                        inline = False
                    )
                    embedHelp.add_field(
                        name   = "```{0}pré-venda``` ou ```{0}pv```".format(PREFIX),
                        value  = messages.helpValues()[6], 
                        inline = False
                    )
                    embedHelp.add_field(
                        name   = "```{}convite```".format(PREFIX),
                        value  = messages.helpValues()[7], 
                        inline = False
                    )
                    embedHelp.add_field(
                        name   = "```{}botinfo```".format(PREFIX),
                        value  = messages.helpValues()[8], 
                        inline = False
                    )
                    embedHelp.add_field(
                        name   = "```{}game [nome do jogo]```".format(PREFIX),
                        value  = messages.helpValues()[9], 
                        inline = False
                    )
                    embedHelp.add_field(
                        name   = "```{}genre [gênero do jogo]```".format(PREFIX),
                        value  = messages.helpValues()[10], 
                        inline = False
                    )
                    embedHelp.add_field(
                        name   = "```{}maxprice [preço]```".format(PREFIX),
                        value  = messages.helpValues()[11], 
                        inline = False
                    )
                    embedHelp.add_field(
                        name   = "```{0}análises [nome do jogo]``` ou ```{0}reviews [nome do jogo]```".format(PREFIX),
                        value  = messages.helpValues()[12], 
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
                            value  = messages.helpValues(img=IMG_GENRES)[0],
                            inline = False
                        )
                        embedHelp.set_footer(text="Utilize {}genre [um dos gêneros acima]".format(PREFIX))

                        await message.channel.send(embed=embedHelp)
                    else:
                        await message.channel.send(messages.commandAlert()[2])

            # Comando: $invite ou $convite
            elif(
                __command__ == "invite" or
                __command__ == "convite"
            ):
                embedInvite = discord.Embed(
                    title       = messages.title()[0],
                    color       = COLOR,
                    description = '**{}**'.format(INVITE)
                )
                embedInvite.set_thumbnail(url=client.user.avatar_url)

                await message.channel.send(embed=embedInvite)

            # Comando: $destaque ou $dt
            elif(
                __command__ == "destaque" or
                __command__ == "dt"
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
                ) = await crawler.getSpotlightOffers()
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

                        x -= 1

            # Comando: $promocao ou $pr
            elif(
                __command__ == "promoção" or
                __command__ == "promocao" or
                __command__ == "pr"
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
                ) = await crawler.getDailyGamesOffers()
                
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
                        
                        x -= 1

            # Comando: $botinfo ou $info
            elif(
                __command__ == "botinfo" or
                __command__ == "info"
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
                    name   = "Sobre {}".format(client.user.name), 
                    value  = messages.infoValues()[2] + 
                    client.get_user(AUTHOR_ID).name + "#" 
                    + client.get_user(AUTHOR_ID).discriminator + "**", 
                    inline = False
                )
                embedBotInfo.set_author(
                    name     = client.get_user(AUTHOR_ID).name + "#" 
                    + client.get_user(AUTHOR_ID).discriminator, 
                    icon_url = client.get_user(AUTHOR_ID).avatar_url
                )
                embedBotInfo.set_footer(
                    text="Criado em 26 de Maio de 2020! | Última atualização em {}."
                    .format(messages.infoValues()[3])
                )

                await message.channel.send(embed=embedBotInfo)

            # Comando: $novidades ou $populares ou $np
            elif(
                __command__ == "novidades" or
                __command__ == "populares" or
                __command__ == "np"
            ):
                (
                    gamesNames, 
                    gamesUrls, 
                    gamesOriginalPrices, 
                    gamesFinalPrices, 
                    gamesImages
                ) = await crawler.getTabContent(URL+'=NewReleases', 'NewReleasesRows')
                
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
                        
                        x -= 1

                    await message.channel.send(member.mention + messages.checkDm())
                    await member.send(messageConcat0)
                    await member.send(messageConcat1)

            # Comando: $maisvendidos ou $mv
            elif(
                __command__ == "mais vendidos" or
                __command__ == "maisvendidos" or
                __command__ == "mv"
            ):
                (
                    gamesNames, 
                    gamesUrls, 
                    gamesOriginalPrices, 
                    gamesFinalPrices, 
                    gamesImages
                ) = await crawler.getTabContent(URL+'=TopSellers', 'TopSellersRows')
                
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
                        
                        x -= 1

                    await message.channel.send(member.mention + messages.checkDm())
                    await member.send(messageConcat0)
                    await member.send(messageConcat1)

            # Comando: $jogospopulares ou $jp
            elif(
                __command__ == "jogos populares" or
                __command__ == "jogospopulares" or
                __command__ == "jp"
            ):
                (
                    gamesNames, 
                    gamesUrls, 
                    gamesOriginalPrices, 
                    gamesFinalPrices, 
                    gamesImages
                ) = await crawler.getTabContent(URL+'=ConcurrentUsers', 'ConcurrentUsersRows')
                
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
                        
                        x -= 1

                    await message.channel.send(member.mention + messages.checkDm())
                    await member.send(messageConcat0)
                    await member.send(messageConcat1)

            # Comando: $prevenda ou $pv
            elif(
                __command__ == "pré-venda" or
                __command__ == "pre-venda" or
                __command__ == "prevenda" or
                __command__ == "pv"
            ):
                (
                    gamesNames, 
                    gamesUrls, 
                    gamesOriginalPrices, 
                    gamesFinalPrices, 
                    gamesImages
                ) = await crawler.getTabContent(URL+'=ComingSoon', 'ComingSoonRows')
                
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
                        
                        x -= 1

                    await message.channel.send(member.mention + messages.checkDm())
                    await member.send(messageConcat0)
                    await member.send(messageConcat1)

            # Comando: $game
            elif(__command__.find("game") == 0):
                gameNameMessage = __command__.split("game ")

                if(len(gameNameMessage) == 1):
                    await message.channel.send(messages.commandAlert(prefix=PREFIX)[0])
                else:
                    gameToSearch = gameNameMessage[1]
                    
                    # Mensagem de busca de jogo, com efeito de carregamento.
                    messageContent    = messages.searchMessage()[1]
                    searchGameMessage = await message.channel.send(messageContent + " __"+ gameToSearch + "__ .**")
                    
                    sleep(0.5)
                    await searchGameMessage.edit(content=messageContent + " __" + gameToSearch + "__ . .**")
                    
                    sleep(0.5)
                    await searchGameMessage.edit(content=messageContent + " __"+ gameToSearch + "__ . . .**")

                    embedSpecificGame = await specificGameEmbed(
                        crawler      = crawler, 
                        embedColor   = COLOR, 
                        gameToSearch = gameToSearch
                    )

                    if(embedSpecificGame != None):
                        await searchGameMessage.edit(content="", embed=embedSpecificGame)
                        await searchGameMessage.add_reaction(REACTION_REVIEW)
                    else:
                        await searchGameMessage.edit(content=messages.noOffers()[2])

            # Comando: $genre
            elif(__command__.find("genre") == 0):
                gameGenreMessage = __command__.split("genre ")

                if(len(gameGenreMessage) == 1):
                    await message.channel.send(messages.commandAlert(prefix=PREFIX)[1])
                else:
                    gameGenreToSearch = gameGenreMessage[1]

                    # Mensagem de busca, com efeito de carregamento.
                    messageContent      = messages.searchMessage()[2]
                    searchGenreMessage  = await message.channel.send(messageContent + " __"+ gameGenreToSearch +"__ .**")
                    
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
                    ) = await crawler.getGameRecommendationByGenre(gameGenreToSearch)

                    if(gameName != None):
                        embedGameRecommendationByGenre = discord.Embed(
                            title = messages.title(genre=gameGenreToSearch)[6],
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
                        await searchGenreMessage.add_reaction(REACTION_REVIEW)
                    else:
                        await searchGenreMessage.edit(content=messages.noOffers(prefix=PREFIX)[3])

            # Comando: $maxprice
            elif(__command__.find("maxprice") == 0):
                maxPriceMessage = __command__.split("maxprice ")
                
                if(len(maxPriceMessage) == 2 and maxPriceMessage[1].isnumeric()):
                    maxPrice          = maxPriceMessage[1]

                    # Mensagem de busca de jogo, com efeito de carregamento.
                    messageContent    = messages.searchMessage()[3]
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
                    ) = await crawler.getGameRecommendationByPriceRange(maxPrice)

                    embedGameRecommendationByPrice = discord.Embed(
                        title = messages.title(gameName=gameName)[7],
                        color = COLOR
                    )
                    embedGameRecommendationByPrice.set_image(url=gameIMG)
                    embedGameRecommendationByPrice.add_field(
                        name   = "**Link:**", 
                        value  = "**[Clique Aqui]({})**".format(gameURL), 
                        inline = False
                    )
                    
                    if(gameOriginalPrice != gameFinalPrice): # Caso o jogo esteja em promoção.
                        embedGameRecommendationByPrice.add_field(
                            name   = "**Preço Original:**", 
                            value  = "**{}**".format(gameOriginalPrice), 
                            inline = True
                        )
                        embedGameRecommendationByPrice.add_field(
                            name   = "**Preço com Desconto:**", 
                            value  = "**{}**".format(gameFinalPrice), 
                            inline = True
                        )
                    else: # Caso o jogo não esteja em promoção.
                        embedGameRecommendationByPrice.add_field(
                            name   = "**Preço:**", 
                            value  = "**{}**".format(gameOriginalPrice), 
                            inline = False
                        )

                    if(int(maxPriceMessage[1]) > 120):
                        embedGameRecommendationByPrice.set_footer(
                            text = messages.recommendationByPrice()[1]
                        )
                    elif(int(maxPriceMessage[1]) < 10):
                        embedGameRecommendationByPrice.set_footer(
                            text = messages.recommendationByPrice()[2]
                        )
                    
                    await searchGameMessage.edit(content="", embed=embedGameRecommendationByPrice)
                    await searchGameMessage.add_reaction(REACTION_REVIEW)
                else:
                    if(len(maxPriceMessage) == 1):
                        await message.channel.send(messages.recommendationByPrice()[3])
                    else:
                        await message.channel.send(messages.recommendationByPrice()[0])
            
            elif(
                __command__.find("análises") == 0 or
                __command__.find("analises") == 0 or
                __command__.find("análise")  == 0 or
                __command__.find("analise")  == 0 or
                __command__.find("reviews")  == 0 or
                __command__.find("review")   == 0
            ):
                if(__command__.find("análises") == 0):
                    gameToSearch = __command__.split("análises")
                elif(__command__.find("analises") == 0):
                    gameToSearch = __command__.split("analises")
                elif(__command__.find("análise") == 0):
                    gameToSearch = __command__.split("análise")
                elif(__command__.find("analise") == 0):
                    gameToSearch = __command__.split("analise")
                elif(__command__.find("reviews") == 0):
                    gameToSearch = __command__.split("reviews")
                elif(__command__.find("review") == 0):
                    gameToSearch = __command__.split("review")

                gameToSearch = gameToSearch[1]

                # Mensagem de busca, com efeito de carregamento.
                messageContent = messages.searchMessage()[0]
                searchMessage  = await message.channel.send(messageContent)
                
                sleep(0.5)
                await searchMessage.edit(content = messageContent+" **.**")
                
                sleep(0.5)
                await searchMessage.edit(content = messageContent+" **. .**")

                # Caso seja passado o link do jogo.
                if(gameToSearch.lower().find("store.steampowered.com/app") != -1):
                    (
                        gameName, 
                        gameIMG, 
                        gameOriginalPrice,
                        gameFinalPrice,
                        gameDescription
                    ) = await crawler.getGameByLink(gameToSearch)

                    searchUrl = None
                    gameURL   = gameToSearch + "?l=brazilian"
                else: # Caso seja passado o nome do jogo.
                    (
                        gameName, 
                        gameURL, 
                        gameIMG, 
                        gameOriginalPrice,
                        gameFinalPrice,
                        searchUrl,
                        gameDescription
                    ) = await crawler.getSpecificGame(gameToSearch)

                if(gameURL != None):
                    embedGameReview = await gameReviewEmbed(
                        crawler    = crawler,
                        embedColor = COLOR,
                        gameUrl    = gameURL,
                        gameName   = gameName,
                        gameIMG    = gameIMG,
                        searchUrl  = searchUrl
                    )

                    await searchMessage.edit(content="", embed=embedGameReview)
                    await searchMessage.add_reaction(REACTION_GAME)
                else:
                    await searchMessage.edit(content=messages.noOffers()[2])
            else:
                await message.channel.send(messages.commandAlert()[2]) 
        else:
            # Caso a mensagem enviada contenha o link de um jogo da Steam.
            if(message.content.lower().find("store.steampowered.com/app") != -1):
                temp = message.content.lower().split("/")
                
                # Caso tenha todos os parâmetros necessários.
                if(len(temp) == 7):
                    gameURL = message.content.lower()

                    (
                        gameName, 
                        gameIMG, 
                        gameOriginalPrice,
                        gameFinalPrice,
                        gameDescription
                    ) = await crawler.getGameByLink(gameURL)

                    embedGameBylink =  discord.Embed(
                        title = "👾 Jogo: {} 👾".format(gameName),
                        color = COLOR
                    )
                    embedGameBylink.set_image(url=gameIMG)
                    embedGameBylink.add_field(
                        name   = "**Link:**", 
                        value  = "**[Clique Aqui]({})**".format(gameURL), 
                        inline = False
                    )

                    if(gameOriginalPrice != gameFinalPrice): # Caso o jogo esteja em promoção.
                        embedGameBylink.add_field(
                            name   = "**Preço Original:**", 
                            value  = "**{}**".format(gameOriginalPrice), 
                            inline = True
                        )
                        embedGameBylink.add_field(
                            name   = "**Preço com Desconto:**", 
                            value  = "**{}**".format(gameFinalPrice), 
                            inline = True
                        )
                    else: # Caso o jogo não esteja em promoção.
                        embedGameBylink.add_field(
                            name   = "**Preço:**", 
                            value  = "**{}**".format(gameOriginalPrice), 
                            inline = False
                        )

                    if(gameDescription != None):
                        embedGameBylink.add_field(
                            name   = "**Descrição:**", 
                            value  = "{}".format(gameDescription), 
                            inline = False
                        )

                    await message.channel.send(embed=embedGameBylink)

@client.event
async def on_reaction_add(reaction, user):
    message = reaction.message

    # Caso a reação seja na mensagem do comando $game, $genre ou $maxprice
    if(
        reaction.emoji                       == REACTION_REVIEW and 
        message.embeds[0].title.find("Jogo") != -1              and
        user.id                              != client.user.id  and
        message.author                       == client.user     and 
        not user.bot
    ):
        # Caso o comando seja $genre
        if(message.embeds[0].title.find("recomendado 🕹️") != -1):
            gameUrlEmbed = message.embeds[0].fields[1].value
            gameName     = message.embeds[0].fields[0].value
        else: # Caso o comando seja $genre ou $maxprice
            gameUrlEmbed   = message.embeds[0].fields[0].value
            temp           = message.embeds[0].title.split(" ")
            gameName       = ""
            x              = 2

            while(temp[x] != "👾" and temp[x] != "💰"):
                gameName += temp[x] + " "
                x        += 1

            gameName = gameName.strip()

        gameUrl = search(r'\((.*?)\)', gameUrlEmbed).group(1)
        gameIMG = message.embeds[0].image.url

        embedGameReview = await gameReviewEmbed(
            crawler    = crawler,
            embedColor = COLOR,
            gameUrl    = gameUrl,
            gameName   = gameName,
            gameIMG    = gameIMG,
            searchUrl  = None
        )

        await message.channel.send(embed=embedGameReview)
    elif(
        reaction.emoji                          == REACTION_GAME  and
        message.embeds[0].title.find("Análise") != -1             and
        user.id                                 != client.user.id and
        message.author                          == client.user    and
        not user.bot
    ):
        temp     = message.embeds[0].title.split(" ")
        gameName = ""
        x        = 2

        while(temp[x] != "👍" and temp[x] != "👎"):
            gameName += temp[x] + " "
            x        += 1

        gameName = gameName.strip()

        embedSpecificGame = await specificGameEmbed(
            crawler          = crawler, 
            embedColor       = COLOR, 
            gameToSearch = gameName
        )

        await message.channel.send(embed=embedSpecificGame)

# Mudar o Status do bot automaticamente e de forma aleatória.
async def changeStatus():
    await client.wait_until_ready()
    await asyncio.sleep(20)
    
    while not client.is_closed():
        numServers   = len(client.guilds)
        msgStatus    = messages.status(PREFIX, numServers)
        randomStatus = messages.randomMessage(msgStatus)
        game         = discord.Game(randomStatus)
        online       = discord.Status.online

        await client.change_presence(status=online, activity=game)
        await asyncio.sleep(20)

client.loop.create_task(changeStatus())

client.run(TOKEN)