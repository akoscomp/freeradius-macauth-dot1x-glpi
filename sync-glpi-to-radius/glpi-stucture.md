# Where GLPI store mac addresses

- Table: glpi_networkports
- Column: mac
- GUI: Computer - Network Ports

Querry:
```
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
```


- Now I skip it, because I don't want to use it
- Table: glpi_items_devicenetworkcards
- Column: mac
- GUI: Setup - Components - Network Cards

Querry:
```
SELECT
  mac,
  glpi_networkports.mac
FROM glpi_items_devicenetworkcards
```
