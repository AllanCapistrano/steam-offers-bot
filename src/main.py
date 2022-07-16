import os
import asyncio

import discord
from discord import User, Reaction
from discord.ext import commands
from dotenv import load_dotenv

from commands.brazilianPortuguese import CommandsBrazilianPortuguese
from commands.english import CommandsEnglish
from services.crawler import Crawler
from services.messages import Message
from services.GameReview.gameReviewEmbed import gameReviewEmbed
from services.SpecificGame.specificGameEmbed import specificGameEmbed
from embeds.embedCurrency import EmbedCurrency

# Permite a leitura do arquivo .env
load_dotenv()

# ------------------------------ Constants ----------------------------------- #
PREFIX          = os.getenv("PREFIX")
COLOR           = 0xa82fd2
INVITE          = "https://discord.com/oauth2/authorize?client_id=714852360241020929&scope=bot&permissions=485440"
TOKEN           = os.getenv("DISCORD_TOKEN")
REACTION_REVIEW = "👍"
REACTION_GAME   = "🎮"
REACTION_NEXT   = "➡️"
REACTION_BACK   = "⬅️"
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
    # Só executa caso a mensagem enviado pelo usuário não seja um comando.
    await client.process_commands(message)

    if(not message.author.bot and message.content.find(PREFIX) == -1):
        # Caso a mensagem enviada contenha o link de um jogo da Steam.
        if(message.content.lower().find("store.steampowered.com/app") != -1):
            temp = message.content.lower().split("/")
            
            # Caso tenha todos os parâmetros necessários.
            if(len(temp) == 7):
                embedGameByLink = await specificGameEmbed(
                    crawler      = crawler,
                    embedColor   = COLOR,
                    gameToSearch = message.content.lower()
                )

                searchGameUrl = await message.channel.send(embed=embedGameByLink)
                await searchGameUrl.add_reaction(REACTION_REVIEW)

@client.event
async def on_reaction_add(reaction: Reaction, user: User):
    message = reaction.message

    # Caso a reação seja na mensagem do comando $game, $genre ou $maxprice
    if(
        reaction.emoji == REACTION_REVIEW and 
        (
            message.embeds[0].title.find("Jogo") != -1 or
            message.embeds[0].title.find("Game") != -1 or
            message.embeds[0].title.find("game") != -1 
        ) and
        user.id        != client.user.id and
        message.author == client.user    and 
        not user.bot
    ):
        language = None if message.embeds[0].title.find("Jogo") != -1 else "english"

        # Caso o comando seja $genre
        if(
            message.embeds[0].title.find("recomendado 🕹️") != -1 or
            message.embeds[0].title.find("🎮 Recommended") != -1
        ):
            gameName     = message.embeds[0].fields[0].value
        else: # Caso o comando seja $genre ou $maxprice
            temp           = message.embeds[0].title.split(" ")
            gameName       = ""
            x              = 2

            while(temp[x] != "👾" and temp[x] != "💰"):
                gameName += temp[x] + " "
                x        += 1

            gameName = gameName.strip()

        embedGameReview = await gameReviewEmbed(
            crawler      = crawler,
            embedColor   = COLOR,
            gameToSearch = gameName,
            language     = language
        )

        await message.channel.send(embed=embedGameReview)
    elif(
        reaction.emoji == REACTION_GAME  and
        (
            message.embeds[0].title.find("Análise") != -1 or
            message.embeds[0].title.find("Review")  != -1
        ) and
        user.id        != client.user.id and
        message.author == client.user    and
        not user.bot
    ):
        language = None if message.embeds[0].title.find("Análise") != -1 else "english"

        temp     = message.embeds[0].title.split(" ")
        gameName = ""
        x        = 2

        while(temp[x] != "👍" and temp[x] != "👎" and temp[x] != "⚠"):
            gameName += temp[x] + " "
            x        += 1

        gameName = gameName.strip()

        embedSpecificGame = await specificGameEmbed(
            crawler      = crawler, 
            embedColor   = COLOR, 
            gameToSearch = gameName,
            currency     = "br" if language == None else "us",
            language     = language
        )

        await message.channel.send(embed=embedSpecificGame)
    elif(
        reaction.emoji                                == REACTION_NEXT and
        (
            message.embeds[0].title.find("Moedas")    != -1 or
            message.embeds[0].title.find("Supported") != -1
        ) and
        user.id                                       != client.user.id and
        not user.bot
    ):
        embedHelpCurrency = EmbedCurrency(
            color   = COLOR,
            message = customMessage
        )

        await reaction.message.remove_reaction(REACTION_NEXT, reaction.message.author)
        await reaction.message.remove_reaction(REACTION_NEXT, user)

        await reaction.message.add_reaction(REACTION_BACK)

        if(message.embeds[0].title.find("Moedas") != -1):
            await reaction.message.edit(
                embed=embedHelpCurrency.embedCurrencyPortuguese(start=24, end=39)
            )
        elif(message.embeds[0].title.find("Supported") != -1):
            await reaction.message.edit(
                embed=embedHelpCurrency.embedCurrencyEnglish(start=24, end=39)
            )
    elif(
        reaction.emoji                                == REACTION_BACK and
        (
            message.embeds[0].title.find("Moedas")    != -1 or
            message.embeds[0].title.find("Supported") != -1
        ) and
        user.id                                       != client.user.id and
        not user.bot
    ):
        embedHelpCurrency = EmbedCurrency(
            color   = COLOR,
            message = customMessage
        )

        await reaction.message.remove_reaction(REACTION_BACK, reaction.message.author)
        await reaction.message.remove_reaction(REACTION_BACK, user)

        await reaction.message.add_reaction(REACTION_NEXT)

        if(message.embeds[0].title.find("Moedas") != -1):
            await reaction.message.edit(
                embed=embedHelpCurrency.embedCurrencyPortuguese(end=24)
            )
        elif(message.embeds[0].title.find("Supported") != -1):
            await reaction.message.edit(
                embed=embedHelpCurrency.embedCurrencyEnglish(end=24)
            )

# Mudar o Status do bot automaticamente e de forma aleatória.
async def changeStatus():
    await client.wait_until_ready()
    await asyncio.sleep(10)
    
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

# Permite que o Bot escute os comandos em Português Brasileiro.
client.add_cog(
    CommandsBrazilianPortuguese(
        client=client, 
        prefix=PREFIX, 
        color=COLOR, 
        urlInvite=INVITE,
        reactions=[REACTION_REVIEW, REACTION_GAME, REACTION_NEXT, REACTION_BACK]
    )
)
# Permite que o Bot escute os comandos em Inglês.
client.add_cog(
    CommandsEnglish(
        client=client, 
        prefix=PREFIX, 
        color=COLOR, 
        urlInvite=INVITE,
        reactions=[REACTION_REVIEW, REACTION_GAME, REACTION_NEXT, REACTION_BACK]
    )
)

client.run(TOKEN)