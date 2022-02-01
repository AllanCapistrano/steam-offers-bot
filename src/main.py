import os
import asyncio
from re import search

import discord
from discord import User, Reaction
from discord.ext import commands
from dotenv import load_dotenv

from commands import Commands
from services.crawler import Crawler
from services.messages import Message
from services.GameReview.gameReviewEmbed import gameReviewEmbed
from services.SpecificGame.specificGameEmbed import specificGameEmbed

# Permite a leitura do arquivo .env
load_dotenv()

# ------------------------------ Constants ----------------------------------- #
PREFIX          = os.getenv("PREFIX")
COLOR           = 0xa82fd2
INVITE          = "https://discord.com/oauth2/authorize?client_id=714852360241020929&scope=bot&permissions=485440"
TOKEN           = os.getenv("DISCORD_TOKEN")
REACTION_REVIEW = "👍"
REACTION_GAME   = "🎮"
# ---------------------------------------------------------------------------- #

intents           = discord.Intents.default()
intents.members   = True
intents.reactions = True

client = commands.Bot(command_prefix=PREFIX, intents=intents)
client.remove_command("help") # Remove o comando help padrão da biblioteca.

crawler       = Crawler()
customMessage = Message()

@client.event
async def on_ready():
    numServers = len(client.guilds)

    print("\n{} está online em {} servidores".format(client.user.name, numServers))

    game   = discord.Game("Online em {} Servidores".format(numServers))
    online = discord.Status.online

    await client.change_presence(status=online, activity=game)

@client.event
async def on_message(message: str):
    if(not message.author.bot):
        # Caso a mensagem enviada contenha o link de um jogo da Steam.
        if(message.content.lower().find("store.steampowered.com/app") != -1):
            temp = message.content.lower().split("/")
            
            # Caso tenha todos os parâmetros necessários.
            if(len(temp) == 7):
                embedGameBylink = await specificGameEmbed(
                    crawler      = crawler,
                    embedColor   = COLOR,
                    gameToSearch = message.content.lower()
                )

                searchGameUrl = await message.channel.send(embed=embedGameBylink)
                await searchGameUrl.add_reaction(REACTION_REVIEW)

    # Só executa caso a mensagem enviado pelo usuário não seja um comando.
    await client.process_commands(message)

@client.event
async def on_reaction_add(reaction: Reaction, user: User):
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

        gameUrl = search(r"\((.*?)\)", gameUrlEmbed).group(1)
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
        msgStatus    = customMessage.status(PREFIX, numServers)
        randomStatus = customMessage.randomMessage(msgStatus)
        game         = discord.Game(randomStatus)
        online       = discord.Status.online

        await client.change_presence(status=online, activity=game)
        await asyncio.sleep(20)

# Cria a task para mudar o status do Bot.
client.loop.create_task(changeStatus())

# Permite que o bot escute os comandos.
client.add_cog(
    Commands(
        client=client, 
        prefix=PREFIX, 
        color=COLOR, 
        urlInvite=INVITE,
        reactions=[REACTION_REVIEW, REACTION_GAME]
    )
)

client.run(TOKEN)