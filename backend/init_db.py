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
        # todo: change the database to the one we want to create
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
        sql = '''CREATE TABLE IF NOT EXISTS offer_test_partition(
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

        # # copy the hotel dataset to the hotel table
        # sql = f'''COPY hotel(hotelid,hotelname,hotelstars)
        # FROM '{env.get('HOTEL_DATA')}'
        # DELIMITER ';'
        # CSV HEADER;'''  

        # print('Inserting the data into the hotels table.')
        # cursor.execute(sql)
        # print('Insertion complete')

        # # copy the offer dataset to the offer table
        # sql = f'''COPY offer(hotelid, \
        # outbounddeparturedatetime, inbounddeparturedatetime, \
        # countadults, countchildren, price, \
        # inbounddepartureairport, inboundarrivalairport, \
        # inboundarrivaldatetime, outbounddepartureairport, \
        # outboundarrivalairport, outboundarrivaldatetime, \
        # mealtype, oceanview, roomtype)
        # FROM '{env.get("OFFER_DATA")}'
        # DELIMITER ';'
        # CSV HEADER;''' 

        # print('Copying the data into the offers table. \
        #       this may take a while...')
        # cursor.execute(sql)
        # print('Insertion complete')

        cursor.close()
        conn.close()

# init database with the corresponding data
db = Database()
db.connect()


#  \COPY offer FROM 'C:\Users\Ronald\Desktop\Scholarships\Check24\holiday-challenge\backend\data\offers.csv\offers.csv' DELIMITER ';' CSV HEADER;
# command: psql -c "command" -U "user" -P "password"? -d "database"









