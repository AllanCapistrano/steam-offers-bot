from catch_offers import CatchOffers
import asyncio
import discord
import discordToken

#Convite discordapp.com/oauth2/authorize?client_id=714852360241020929&scope=bot&permissions=485440

'''if __name__ == '__main__':
    catchOffers = CatchOffers()

    testeURL, testeIMG = catchOffers.getDailyGamesOffers()
    testeOri, testeFin = catchOffers.getDailyGamesOffersPrices()

    print('URL: ' + str(testeURL))
    print('Imagem: ' + str(testeIMG))
    print('Original: ' + str(testeOri))
    print('Final: ' + str(testeFin))

    testeURL_2, testeIMG_2 = catchOffers.getSpotlightOffers()

    print('URL: ' + str(testeURL_2) + '\n')
    print('Imagem: ' + str(testeIMG_2) + '\n')

    print('H2: ' + str(catchOffers.getSpotlightOffersContentH2()))'''

TOKEN = discordToken.myToken()
client = discord.Client()
member = discord.Member #Verificar se vai precisar
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
        embedHelp.add_field(name = "```$botinfo```", value = "**Exibe as informações do Bot e do criador do mesmo.**", inline = False)

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
        #list_H2 = catchOffers.getSpotlightOffersContentH2()
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


client.run(TOKEN)