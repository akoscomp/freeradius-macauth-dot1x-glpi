db_user="root"
db_pass="sVmWfe9ugUsAYHWKbnyu6c8m" # mysql root password from mariadb/.env
db_host="lan-db-mariadb"
db_port=3306


# Define queries, can delete it, is only for test
select_mac_cname_vlan_query = """
SELECT
  glpi_computers.name,
  glpi_networkports.mac,
  glpi_vlans.name,
  glpi_vlans.tag
FROM glpi_computers
JOIN glpi_networkports
  ON glpi_computers.id = glpi_networkports.items_id
JOIN glpi_networkports_vlans
  ON glpi_networkports.id = glpi_networkports_vlans.networkports_id
JOIN glpi_vlans
  ON glpi_vlans.id = glpi_networkports_vlans.vlans_id
"""

select_mac_vlan_query = """
SELECT
  glpi_networkports.mac,
  glpi_vlans.name,
  glpi_vlans.tag
FROM glpi_networkports
JOIN glpi_networkports_vlans
  ON glpi_networkports.id = glpi_networkports_vlans.networkports_id
JOIN glpi_vlans
  ON glpi_vlans.id = glpi_networkports_vlans.vlans_id
"""

select_mac_cname_query = """
SELECT
  glpi_computers.name,
  glpi_networkports.mac
FROM glpi_computers
JOIN glpi_networkports
  ON glpi_computers.id = glpi_networkports.items_id
"""

insert_to_radreply_q1 = """
INSERT INTO
  radreply
  (username, attribute, op, value)
VALUES
  ("00:00:00:00:00:00", "Tunnel-Type", "=", "VLAN")
"""
insert_to_radreply_q2 = """
INSERT INTO
  radreply
  (username, attribute, op, value)
VALUES
  ("00:00:00:00:00:00", "Tunnel-Medium-Type", "=", "IEEE-802")
"""
insert_to_radreply_q3 = """
INSERT INTO
  radreply
  (username, attribute, op, value)
VALUES
  ("00:00:00:00:00:00", "Tunnel-Private-Group-Id", "=", "1111")
"""

#cursor.executemany(q1, q2)
