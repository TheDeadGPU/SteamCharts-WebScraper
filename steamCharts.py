#James J Girard
import requests
import pandas as pd
import sqlite3
import lxml.html
#Instantiate Variables 
tableElements = list()
data = {
    "rank": [],
    "name": [],
    "current_players": [],
    "peak_players": [],
    "hours_played": []
}

#Gather our data from the internet
print("Gathering Steam Game Statistics (Last 30 Days). This may take a few moments.")
for i in range(1,41):
    r = requests.get("https://steamcharts.com/top/p." + str(i))
    html = lxml.html.fromstring(r.text)
    top_games_table = html.get_element_by_id("top-games")
    tableElements = top_games_table.getchildren()[1].getchildren()
    #Import our data into Pandas DataFrame
    for element in tableElements:
        cells = element.getchildren()
        data["rank"].append(int(str(cells[0].text_content().strip()).replace(".","")))
        data["name"].append(cells[1].text_content().strip())
        data["current_players"].append(int(cells[2].text_content().strip()))
        data["peak_players"].append(int(cells[4].text_content().strip()))
        data["hours_played"].append(int(cells[5].text_content().strip()))

#Create the Database
db = sqlite3.connect(":memory:")
cursor = db.cursor()
cursor.execute(""" CREATE TABLE STEAMGAMES(RANK,NAME,CURRENT_PLAYERS,PEAK_PLAYERS,HOURS_PLAYED)""")
#Dump the Dataframe into SQLITE
df = pd.DataFrame(data)
for row in df.itertuples():
    sqlCode = """ INSERT INTO STEAMGAMES(RANK,NAME,CURRENT_PLAYERS,PEAK_PLAYERS,HOURS_PLAYED)
                VALUES(?,?,?,?,?)"""
    cursor.execute(sqlCode,row[1:])
    db.commit()
#Display the database contents
print("\nDatabase Contents:")
for sqlRow in cursor.execute("""SELECT * FROM STEAMGAMES"""):
    print(sqlRow)
#Display Games with over 100,000 Peak Players
print("\nGames with over 100,000 Peak Players:")
for game in cursor.execute("""SELECT * FROM STEAMGAMES WHERE PEAK_PLAYERS > 100000"""):
    print(game)
#Display Games with Current Players between 10,000 - 100,000 Players
print("\nGames with current players between 10,000 and 100,000 players:")
for game in cursor.execute("""SELECT * FROM STEAMGAMES WHERE (CURRENT_PLAYERS < 100000 AND CURRENT_PLAYERS > 10000)"""):
    print(game)
#Display Games that have over 2,000,000 hours played
print("\nGames that have over 2,000,000 hours played:")
for game in cursor.execute("""SELECT * FROM STEAMGAMES WHERE HOURS_PLAYED > 2000000"""):
    print(game)
db.close()


