import discord
import os
import random
import time
import requests
from datetime import date,timedelta,datetime
import messages
import json
import statements
import apihelper
import asyncio
import callgame
from discord.ext import commands
from keep_alive import keep_alive 
from replit import db
import queue

db_host = 'adjutant-zach-9759.aivencloud.com'
db_name = 'defaultdb'
bottoken = os.environ['bot_token']
websterkey = os.environ['websterkey']
client = discord.Client()
users = ['Chomper#4072','demie#2551','Captain Bulbarus#2248','Ascendance#5342','Ginchey#8598','Alpal Esq.#6166','baramz#7249','El Hobo#2195','Chazington#9943','Doozy#5338']
me = 'Ascendance#5342'
current_date = str(date.today())
db["fastpass"] = []
fastpassqueue = queue.Queue()


@commands.command
async def mention_ping(ctx, member : discord.Member):
  await ctx.send(member)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

async def check_date_and_reset_waifu(message):
  global current_date
  print(current_date)
  if (str(date.today()) != current_date):
    current_date = str(date.today())
    print("Current date changed to "+current_date)
    await reset_db_waifu(message)

async def reset_db_waifu(message):
    for i in users:
      try:
        db[str(i)+'exp'][0] = db[str(i)+'exp'][3]+3
        print(db[str(i)+'exp'])
      except:
        await message.channel.send('Error parsing user '+i)
    await message.channel.send('Waifu rolls for the day have been manually reset.')

#Event that monitors discord messages
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  print(current_date)
  content = message.content.lower()
  author = message.author



  if content.startswith('$countstart') and str(message.author) == me:
    db['dailycounter'] = 0
    print('Counting down.')
    
  if content.startswith('$wreset') and str(message.author) == me:
    await reset_db_waifu(message)
  
  if content.startswith('$dbreset') and str(message.author) == me:
    for i in users:
      db[str(i)+'exp'] = [3,0,10,1]
      
  if content.startswith('$getusers') and str(message.author) == me:
    for i in users:
      print(db[i+'exp'])
  
  if content == ('$fastpass'):
    if author.name in db['fastpass']:
      await message.channel.send('You are already in queue!')
    else:
      for i in db['fastpass']:
        print(i)
      fastpassqueue.put(author.name)
      db['fastpass'].append(author.name)
      await message.channel.send(author.name+" has been added to the fastpass queue.")
  
  if content.startswith('$checkpass'):
    if fastpassqueue.empty() == False:
      await message.channel.send("The fastpass queue is as follows:")
      for i in db['fastpass']:
        await message.channel.send(i)
    else:
      await message.channel.send("The fastpass queue is empty.")

  
  if content.startswith('$nextinline'):
    player = fastpassqueue.get()
    if player == author.name:
      db['fastpass'].remove(author.name)
      await message.channel.send(player+" is up!")
    else:
      message.channel.send("You can't dequeue someone else!")


  
  if content.startswith('$hola') or content.startswith("$hello"):
    await messages.hello(message)
    
  if content.startswith('$experts'):
    await messages.experts(message)
    
  if content == ('$checktime'):
    print(db['dailycounter'])

  if content.startswith('$lookup'):
    try:
      words = content.split(' ')
      word = ''
      idx = 1
      for i in words:
        if idx < len(words):
          word += words[idx]
          idx += 1
      url = str("https://dictionaryapi.com/api/v3/references/spanish/json/"+word +"?key="+websterkey)
      await apihelper.look(url, message)
      
    except:
      await messages.badlookup(message)

  if content.startswith('$help'):
    await messages.help(message)
    

  if content.startswith('$waifu'):
    categories = ['waifu','neko','shinobu','megumin','bully','cuddle','cry','hug',
    'lick','pat','smug','bonk','yeet','blush','smile','wave','nom','bite','slap',
    'kill','kick','happy','wink','poke','dance','cringe']
    types = ['sfw','nsfw']
    print(db.get('reset'))
    if '-type' in message.content:
      split = content.split(' ')
      idx = split.index('-type')
      typewaifu = split[idx+1]
      if typewaifu not in types:
        await message.channel.send("Sorry, the type you've selected is invalid. Please choose from: sfw, nsfw")
    else: 
      typewaifu = 'sfw'
    
    if '-category' in message.content:
      split = content.split(' ')
      idx = split.index('-category')
      categorywaifu = split[idx+1]
      if categorywaifu not in categories:
        await message.channel.send("Sorry, the category you've selected is invalid. Please choose from: waifu, neko, shinobu, megumin, bully, cuddle, cry, hug, lick, pat, smug, bonk, yeet, blush, smile, wave, nom, bite, slap, kill, kick,happy, wink, poke, dance or cringe.")
    else:
      if typewaifu == 'nsfw':
        nsfwcategories = ['waifu','neko']
        categorywaifu = random.choice(nsfwcategories)
      else:
        categorywaifu = random.choice(categories)
    

    response = requests.get('https://api.waifu.pics/'+typewaifu+'/'+categorywaifu)
    dict = response.json()
    db['latest'] = dict['url']
    
    print(message.author.name+'-'+categorywaifu)
    await check_date_and_reset_waifu(message)
    if db[str(message.author)+"exp"][0] <= 0:
      await message.channel.send('Sorry, you\'ve run out of waifu rolls for the day. :(')
      return
    else:
      db[str(message.author)+"exp"][0] -= 1
    await message.channel.send(dict['url'])
    await message.channel.send('You have '+str(db[str(message.author)+"exp"][0])+' waifu rolls left for the day.')
    return
    
  if content.startswith('$dog'):
    response = requests.get('https://dog.ceo/api/breeds/image/random')
    dict = response.json()
    
    await message.channel.send(statements.pick_aww_dog())
    await message.channel.send(dict['message'])

  if content.startswith('$thirsty'):
    response = requests.get('http://www.thecocktaildb.com/api/json/v1/1/random.php')
    dict = json.loads(response)
    
    for i in dict:
      print(i)
      #await message.channel.send('Name: '+dict['drinks'])
      #await message.channel.send('Type: '+dict['drinks'])
      #await message.channel.send('Instructions: '+dict['drinks'])
    
  if content.startswith('$call'):
    game = content.replace('$call ', '').lower()
    players = callgame.call(game)
    await message.channel.send('CALLING ALL BOYS for: '+game)
    for i in players:
      await message.channel.send()
      
    await message.channel.send('CALLING ALL BOYS FOR: '+game+"!")

  if content.startswith('$rps'):
    
    await message.channel.send('Alright, let\'s play.')
    try:
      cheat = random.randint(1,100)
      message = await client.wait_for('message', timeout=7.0)
      if cheat > 50:
        choice = message.content
        choice.lower()
        if choice == 'paper':
          await message.channel.send('I choose scissors, and am definitely not cheating!')
        if choice == 'rock':
          await message.channel.send('I choose paper, and am definitely not cheating!')
        if choice == 'scissors': 
          await message.channel.send('I choose rock, and am definitely not cheating!')
      else:
        list = ['rock', 'paper', 'scissors']
        rand = random.choice(list)
        await message.channel.send('I choose '+rand+'!')
    except asyncio.TimeoutError:
      return await message.channel.send('You took too long!')
    
  if content.startswith('$countdown'):
    
    seconds = content.replace('$countdown ', '').lower()
    try:
      seconds = int(seconds)
    except:
      await message.channel.send('Please enter a valid number of seconds.')
    if seconds > 30:
      seconds = 30
    while seconds != 0:
      time.sleep(1)
      await message.channel.send(seconds)
      seconds = seconds - 1
    
  if content.startswith('$nuke'):
    
    await message.channel.send(';;play https://www.youtube.com/watch?v=04FfDVZ1O14&ab_channel=SKwon')
  
  if content.startswith('$inspire'):
    
    response = requests.get('https://quotesondesign.com/wp-json/wp/v2/posts/?orderby=rand')
    dict = response.json()
    quote = dict['quote']+' - '+dict['author']
    await message.channel.send(quote)
  
  if content.startswith('$joke'):
    
    response = requests.get('https://icanhazdadjoke.com/slack')
    dict = response.json()
    await message.channel.send(dict['attachments'][0]['text'])
  
  if content == '$setbis':
    
    db[str(message.author)+'bis'] = db['latest']
    await message.channel.send(message.author.name+' got BiS!\n''Saved favorite for: '+message.author.name)
    print('Saved favorite: '+ message.author.name)
  
  if content == '$bis':
    await message.channel.send(db[str(message.author)+'bis'])


keep_alive()
client.run(bottoken)
