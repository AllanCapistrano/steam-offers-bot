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

    print(catchOffers.getSpotlightOffersContentH2())'''

TOKEN = discordToken.myToken()
client = discord.Client()
member = discord.Member #Verificar se vai precisar
color = 0x145d8f

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
        embedHelp.set_author(name = "SteamOffersBot lista de comandos:", icon_url = "https://cdn.discordapp.com/app-icons/714852360241020929/cc4cb28bc50ec9ac344a5584a4a13303.png?size=64")
        embedHelp.add_field(name = "```$promocao```", value = "Exibe quais jogos estão na promoção diária da Steam ou gratuitos por um tempo limitado.", inline = False)
        embedHelp.add_field(name = "```$destaque```", value = "Exibe os eventos que estão em destaque na Steam, ou os jogos em promoção que estão em destaque na loja.", inline = False)
        embedHelp.add_field(name = "```$botinfo```", value = "Exibe as informações do Bot e do criador do mesmo.", inline = False)

        await message.channel.send(embed = embedHelp)

    if(message.content.lower().startswith("$destaque")):
        catchOffers = CatchOffers()
        list_gamesURl, list_gamesIMG = catchOffers.getSpotlightOffers()
        x = len(list_gamesURl)

        while(x > 0):
            embedSpotlightGames = discord.Embed(
                title = "🎮 Jogos em Destaque 🎮",
                color = color
            )
            embedSpotlightGames.set_image(url = list_gamesIMG[x - 1])
            embedSpotlightGames.add_field(name = "Link:", value = list_gamesURl[x - 1], inline = False)

            await message.channel.send(embed = embedSpotlightGames)

            x = x - 1
            print("debug " + str(len(list_gamesURl)))

client.run(TOKEN)