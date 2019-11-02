import sqlite3 as lite

con = lite.connect('finalest.sqlite3')
cur = con.cursor()
cur.execute('SELECT "text", "artist", "song" from "songdata_compressed" ')
data = cur.fetchall()

songs = set()
for each in data:
    songs.add(each[2])
    # print(each[2])
print(songs)