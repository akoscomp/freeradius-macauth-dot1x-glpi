from config import *

import mariadb

# Check if mac address exists in radius database
# return mac address count
def check_radius_db_mac_exist(radius_table, mac_address):
    query = """SELECT count(username) FROM {} WHERE username = "{}";""".format(radius_table, mac_address)
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
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results[0][0]

# Check if network port has vlan assigned
def check_glpi_networkport_has_vlan(networkports_id, mac_address):
    query = """
    SELECT
      glpi_networkports.mac,
      glpi_vlans.name,
      glpi_vlans.tag
    FROM glpi_networkports
    JOIN glpi_networkports_vlans
      ON glpi_networkports.id = glpi_networkports_vlans.networkports_id
    JOIN glpi_vlans
      ON glpi_vlans.id = glpi_networkports_vlans.vlans_id
    WHERE
      glpi_networkports.mac = "{}"
    LIMIT 1
    """.format(mac_address)
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
    if len(results) > 0:
      mac_address = results[0][0]
      vlan_name = results[0][1]
      vlan_id = results[0][2]
      return results
    else:
      return False

def check_radius_reply_vlan_id(mac_address):
    query = """
    SELECT
      value
    FROM radreply
    WHERE
      attribute = "Tunnel-Private-Group-Id"
    AND
      username = "{}"
    LIMIT 1
    """.format(mac_address)
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
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results[0][0]

# Select from glpi database mac addresses and device name
# Inpute: table name of the device type, device type string
# Retrun: device name, mac address, networkports_id
def select_glpi_device_by_mac_type(device_table, device_type):
    query = """
        SELECT
          {device_table}.name,
          glpi_networkports.mac,
          glpi_networkports.id
        FROM {device_table}
        JOIN glpi_networkports
          ON {device_table}.id = glpi_networkports.items_id
        WHERE
          glpi_networkports.mac != ""
        AND
          glpi_networkports.itemtype = "{device_type}"
        AND
          {device_table}.is_template = 0
        AND
          {device_table}.is_deleted = 0
    """.format(device_table = device_table, device_type = device_type)
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
    results = list(cursor.fetchall())
    cursor.close()
    connection.close()
    return results

# Need to check itemtype and get other mac types: Monitor, Phone, Peripheral, Printer, Enclosures, PDU, NetworkEquipment
def select_glpi_device_by_mac():
  #Type can be: Computer, Monitor, Phone, Peripheral, Printer, NetworkEquipment
  computer = select_glpi_device_by_mac_type("glpi_computers", "Computer")
  monitor = select_glpi_device_by_mac_type("glpi_monitors", "Monitor")
  phone = select_glpi_device_by_mac_type("glpi_phones", "Phone")
  peripheral = select_glpi_device_by_mac_type("glpi_peripherals", "Peripheral")
  printer = select_glpi_device_by_mac_type("glpi_printers", "Printer")
  allDevies = computer + monitor + phone + peripheral + printer
  return allDevies

# Insert vlan info
def insert_radius_radreply_message(mac_address, vlan_id):
    print("insert_radius_radreply_message")
    attribute = "Tunnel-Type"
    op = "="
    value = "VLAN"
    query1 = """
      INSERT INTO radreply (username,attribute,op,value)
      VALUES ("{}", "{}", "{}", "{}")
    """.format(mac_address, attribute, op, value)
    attribute = "Tunnel-Medium-Type"
    op = "="
    value = "IEEE-802"
    query2 = """
      INSERT INTO radreply (username,attribute,op,value)
      VALUES ("{}", "{}", "{}", "{}")
    """.format(mac_address, attribute, op, value)
    attribute = "Tunnel-Private-Group-Id"
    op = "="
    value = vlan_id
    query3 = """
      INSERT INTO radreply (username,attribute,op,value)
      VALUES ("{}", "{}", "{}", "{}")
    """.format(mac_address, attribute, op, value)
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
    cursor.execute(query1)
    cursor.execute(query2)
    cursor.execute(query3)
    connection.commit()
    cursor.close()
    connection.close()
    return True

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

# Delete mac address from radius replay table
def delete_mac_radius_reply(mac_address):
    query = """
      DELETE FROM
        radreply
      WHERE
        username = "{}";
    """.format(mac_address)
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
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()
    return True

def update_radius_radreply_vlan_id(mac_address, vlan_id):
    query = """
    UPDATE
      radreply
    SET
      value = "{}"
    WHERE
      attribute = "Tunnel-Private-Group-Id"
    AND
      username = "{}"
    """.format(vlan_id, mac_address)
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
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()
    return True
