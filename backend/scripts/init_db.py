import psycopg2
from dotenv import load_dotenv
import os

load_dotenv(".env")

class Database():
    # connects to the database. 
    # Create the database and tables if they do not exist. 

    def connect(self):
        env = os.environ

        # establishing the connection
        conn = psycopg2.connect(
            database=env.get("DATABASE_NAME"), 
            user=env.get("PG_USERNAME"), 
            password=env.get("PG_PASSWORD"), 
            host=env.get("HOST"), 
            port= env.get("PORT")
        )
        conn.autocommit = True

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        # Create hotel table if it does not exist
        sql = '''CREATE TABLE IF NOT EXISTS hotel(
        hotelid INT PRIMARY KEY,
        hotelname VARCHAR(255) NOT NULL,
        hotelstars FLOAT
        )'''

        # execute the command
        cursor.execute(sql)
        print("Hotel table created successfully.")
        
        # Create offer table if it does not exist
        sql = '''CREATE TABLE IF NOT EXISTS offer(
        hotelid INT,
        outbounddeparturedatetime TIMESTAMP,
        inbounddeparturedatetime TIMESTAMP,
        countadults INT,
        countchildren INT,
        price FLOAT,
        inbounddepartureairport CHAR(3),
        inboundarrivalairport CHAR(3),
        inboundarrivaldatetime TIMESTAMP,
        outbounddepartureairport CHAR(3),
        outboundarrivalairport CHAR(3),
        outboundarrivaldatetime TIMESTAMP,
        mealtype VARCHAR(50),
        oceanview BOOLEAN,
        roomtype VARCHAR(50),
        FOREIGN KEY (hotelid) REFERENCES hotel (hotelid)
        );'''

        # execute the command
        cursor.execute(sql)
        print("Offer table created successfully.")

        cursor.close()
        conn.close()

# init database with the corresponding data
db = Database()
db.connect()









