import discord
import random
import statements
from replit import db

async def send(message, channel):
  await channel.send(message)

async def hello(message):
  await send('Hola, '+str(message.author.name)+'!', message.channel)

async def experts(message):
  await send('Here are a list of all the Spanish experts in the world:', message.channel)
  for key in db:
    if db[key] == "Expert":
      await send(key + " - " + db['ChomperStory'], message.channel)
      await send('-End list of world experts-', message.channel)

async def lookup(header, message):
  await send("I searched tirelessly and found this:", message.channel)
  await send(header, message.channel)
  await send("Hope that helps!", message.channel)
  return

async def badlookup(message):
  await send('Oops, for some reason, I am unable look that up.', message.channel)

async def help(message):
  await send('List of all the commands available: \n $hola or $hello - Receive a greeting. \n $experts - Displays a list of Spanish experts of the world. \n $lookup - Translates words from Spanish to English or English to Spanish (Does not work on phrases or full sentences. \n $waifu - Rolls a picture of a Waifu. \n $dog - Displays a random picture of a dog. \n $rps - Play rock-paper-scissors with the bot!', message.channel)

async def yourturn(message):
  await send('Go ahead, its your turn.', message.channel)
