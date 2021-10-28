import sqlite3

#Creates the table. Only available through admin request. Good to use.
def createtable():
  conn = sqlite3.connect('adjutant.db')
  cur = conn.cursor()
  cur.execute("""CREATE TABLE memers (
    name text,
    exp integer,
    nextlevel integer,
    level integer,
    fav text,
    rolls integer
  )""")
  conn.commit()

#Deletes a table. Only available through admin request. Good to use.
def deletetable():
  conn = sqlite3.connect('adjutant.db')
  cur = conn.cursor()  
  cur.execute("""DROP TABLE memers""")



def addnewuser(name):
  conn = sqlite3.connect('adjutant.db')
  cur = conn.cursor()
  cur.execute("""INSERT INTO memers VALUES (user, 0, 10, 1, "", 3)""")
  conn.commit()

#Adds all users in a list. Good to use.

def addallusers(names):
  conn = sqlite3.connect('adjutant.db')
  cur = conn.cursor()
  for name in names:
    cur.execute("INSERT INTO memers VALUES (:name, :exp, :nextlevel, :level, :fav, :rolls)",{'name':name,'exp':0,'nextlevel':10,'level':1,'fav':"",'rolls':3})
  conn.commit()



def getlevel(name):
  conn = sqlite3.connect('adjutant.db')
  cur = conn.cursor()
  q = cur.execute("SELECT level FROM memers WHERE name=name",{'name':name})
  return q[0]

def getrolls(name):
  conn = sqlite3.connect('adjutant.db')
  cur = conn.cursor()
  q = cur.execute("SELECT rolls FROM memers WHERE name=name",{'name':name})
  return q[0]

  

def getallusers():
  conn = sqlite3.connect('adjutant.db')
  cur = conn.cursor()
  cur.execute("""SELECT * FROM memers""")
  q = cur.fetchall()
  for i in q:
    print(i)

# Main get exp function that should run after almost every message. Good to use.

def getexp(name):
  conn = sqlite3.connect('adjutant.db')
  cur = conn.cursor()
  cur.execute("SELECT exp, nextlevel, level FROM memers WHERE name=?",(name))
  q = cur.fetchone()
  if q[0] >= q[1]:
    exp = q[0]-q[1]
    nextlevel = q[1]*2
    level = q[2]+1
    cur.execute("UPDATE memers SET exp =? WHERE name =?",(exp,name))
    cur.execute("UPDATE memers SET nextlevel =? WHERE name =?",(nextlevel,name))
    cur.execute("UPDATE memers SET level =? WHERE name =?",(level,name))    
    conn.commit()
    conn.close()
    return level

# User requested exp. Good to use.

def requestexp(name):
  conn = sqlite3.connect('adjutant.db')
  cur = conn.cursor()
  cur.execute("SELECT exp, nextlevel FROM memers WHERE name = name",{'name': name})
  rows = cur.fetchone()
  percent = (rows[0]/rows[1])*100
  return percent

def addexp(name, points):
  conn = sqlite3.connect('adjutant.db')
  cur = conn.cursor()
  cur.execute("SELECT exp FROM memers WHERE name = name",{'name': name})
  q = cur.fetchone()
  xp = q[0] + points
  print(xp)
  cur.execute("UPDATE memers SET exp=? WHERE name =?",(xp,name))
  cur.execute("SELECT exp FROM memers WHERE name = name",{'name': name})
  q = cur.fetchone()
  print(q[0])
  conn.commit()
  conn.close()
  

def subrolls(name, change):
  conn = sqlite3.connect('adjutant.db')
  cur = conn.cursor()
  q = cur.execute("SELECT rolls FROM memers WHERE name= name")
  rows = q.fetchone()
  rolls = rows[0]-1
  cur.execute("UPDATE memers SET rolls =? WHERE name =?",(rolls,name))
  conn.commit()
  conn.close()

def resetrolls(name):
  conn = sqlite3.connect('adjutant.db')
  cur = conn.cursor()
  q = cur.execute("SELECT rolls, level FROM memers WHERE name='name'",{'name': name})
  level = q[1]
  rolls = 3+level
  cur.execute("UPDATE memers SET rolls = rolls WHERE name = name",{'name': name},{'rolls': rolls})

