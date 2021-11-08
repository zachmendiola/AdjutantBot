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
  await send('List of all the commands available:',message.channel)
  await send('$hola or $hello - Receive a greeting.',message.channel)
  await send('$experts - Displays a list of Spanish experts of the world.',message.channel)
  await send('$lookup - Translates words from Spanish to English or English to Spanish',message.channel)
  await send('$waifu - Rolls a picture of a Waifu. Can add -type tag to decide what type will be rolled.\n    Available types:\n    waifu, neko, shinobu, megumin, bully, cuddle, cry, hug, lick, pat, smug, bonk,\n    blush, smile, wave, nom, bite, slap, kill, kick, happy, wink, poke, dance and cringe',message.channel)
  await send('$fastpass - enqueues the user into the fastpass queue.',message.channel)
  await send('$checkpass - prints out the current queue in order, last being next in line.',message.channel)
  await send('$nextinline - dequeues the player from the queue.',message.channel)
  await send('$dog - Displays a random picture of a dog.',message.channel)
  await send('$rps - Play rock-paper-scissors with the bot!',message.channel)


async def yourturn(message):
  await send('Go ahead, its your turn.', message.channel)
