import messages
import requests

async def look(url, message):
  response = requests.get(url)
  dict = response.json()
  i = 0
  list = []
  for entry in dict:
    header = dict[i]['hwi']['hw'] + " -"
  for item in dict[i]['shortdef']:
    header += " " + item
    list.append(header)
    i += 1
  for item in list:
    print(item)
  await messages.lookup(header, message)
  