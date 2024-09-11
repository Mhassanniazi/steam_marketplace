import pandas as pd
from db import database
import os

def generate_report():
    db, cursor = database.create_connection(parse=True)

    # TODO: Get All Items
    print("-> Extracting Data From Database.")
    data_query = "SELECT game AS 'Game',item AS 'Item',type AS 'Type',listings AS 'Listings',price AS 'Price',description AS 'Description',icon AS 'Icon',url AS 'Product URL' FROM items ORDER BY game"
    cursor.execute(data_query)
    data = cursor.fetchall()
    data_df = pd.DataFrame(data)

    # TODO: Get Items Stats
    print("-> Transforming Data Stats.")
    stats_query = """SELECT game AS 'Game', COUNT(item) AS `Items Count`
    FROM items
    GROUP BY game
    ORDER BY `Items Count` DESC;"""
    cursor.execute(stats_query)
    stats = cursor.fetchall()
    stats_df = pd.DataFrame(stats)

    # TODO: Check Directory
    if not os.path.exists(FOLDER_PATH):
        os.makedirs(FOLDER_PATH)

    # TODO: Export Data
    print("-> Loading Data into Excel Sheet.")
    with pd.ExcelWriter("data/SteamMarketPlace.xlsx") as writer:
        data_df.to_excel(writer, sheet_name="Games", index=False)
        stats_df.to_excel(writer, sheet_name="Stats", index=False)
    
    database.close_connection(cursor, db)

FOLDER_NAME = "data"
FOLDER_PATH = os.path.join(os.getcwd(), FOLDER_NAME)

if __name__ == "__main__":
    generate_report()
    print("✔ All Steps Done.")