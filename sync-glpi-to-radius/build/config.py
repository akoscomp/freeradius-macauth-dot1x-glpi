db_user="root"
db_pass="sVmWfe9ugUsAYHWKbnyu6c8m"
db_host="lan-db-mariadb"
db_port=3306


# Define queries
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

select_mac_cname_query = """
SELECT
  glpi_computers.name,
  glpi_networkports.mac
FROM glpi_computers
JOIN glpi_networkports
  ON glpi_computers.id = glpi_networkports.items_id
"""
