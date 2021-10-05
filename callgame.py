
players = ['Chomper#4072','demie#2551','Captain Bulbarus#2248','Ascendance#5342','Ginchey#8598','Alpal Esq.#6166','baramz#7249','El Hobo#2195']

def call(game):
  list = []
  if game == 'valorant':
    for i in players:
      list.append(i)
    return list
  
  if game == 'catan':
    for i in players:
      list.append(i)
    return list
  
  if game == 'league':
    list.append(players[0],players[1],players[2],players[4],players[5],players[6],players[7])
    return list