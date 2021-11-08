from replit import db
import discord

async def check_exp(name, channel):
  if (db[name+'exp'][1] >= db[name+'exp'][2]):
    db[name+'exp'][2] = db[name+'exp'][2]*10
    db[name+'exp'][3] += 1
    db[name+'exp'][0] = db[name+'exp'][3] + 3
    print('Exp check success for '+name)
    print(db[name+'exp'][1])
    print(db[name+'exp'][2])
    await new_lvl(name, channel)
  else:
    print(name+' has not met required exp to level up.')
    print(db[name+'exp'][1])
    print(db[name+'exp'][2])

def add_exp(name, value):
  try:
    db[name+'exp'][1] += value
  except:
    print('There was an error adding exp for user: '+name)

async def new_lvl(name, channel):
  await channel.send(name+" has leveled up to level: "+str(db[name+'exp'][3])+ " Congrats!")
  