import sys
import time
#import mysql.connector
import mariadb

print("Hello World!")
while False:
    print("in loop")

    #check if task is done
    if(1 == 2):
        print("All done!")
        break
    else:
        time.sleep(600)
        continue

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="root",
        password="sVmWfe9ugUsAYHWKbnyu6c8m",
        host="lan-db-mariadb",
        port=3306,
        database="glpi"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

cur.execute(
    "SELECT name,serial FROM glpi_computers")

# Print Result-set
for (name, serial) in cur:
    print(f"Name: {name}, serial: {serial}")
