from config import *

import mariadb

# Check if mac address exists in radius database
def check_radius_db_mac_exist(mac_address):
    query = "SELECT count(username) FROM radcheck WHERE username=?;"
    db_database="radius"

    try:
        connection = mariadb.connect(
            user=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            database=db_database
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    cursor = connection.cursor()
    cursor.execute(query, [mac_address])
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results[0][0]

# Select from glpi database mac addresses and computer names
def select_glpi_mac_computername():
    query = """
        SELECT
          glpi_computers.name,
          glpi_networkports.mac
        FROM glpi_computers
        JOIN glpi_networkports
          ON glpi_computers.id = glpi_networkports.items_id
    """
    db_database="glpi"

    try:
        connection = mariadb.connect(
            user=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            database=db_database
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

# Insert into radius database mac address and computer name
def insert_radius_mac_computername(mac_address, computer_name):
    attribute = "Cleartext-Password"
    op = ":="
    query = """
      INSERT INTO radcheck (username,attribute,op,value,comment)
      VALUES (?, ?, ?, ?, ?)
    """
    db_database="radius"

    try:
        connection = mariadb.connect(
            user=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            database=db_database
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    cursor = connection.cursor()
    cursor.execute(query, (mac_address, attribute, op, mac_address, computer_name))
    connection.commit()
    cursor.close()
    connection.close()
    return True
