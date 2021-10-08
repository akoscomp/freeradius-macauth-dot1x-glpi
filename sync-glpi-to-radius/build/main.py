import time

from config import *
from functions import *

print("Hello, I'm GLPI and Radius DB sync!")

# Copy data
for (computer_name, mac_address, networkports_id) in select_glpi_mac_computername():
  print(f"Check mac: {mac_address}")
  if check_radius_db_mac_exist("radcheck", mac_address) == 0:
    if insert_radius_mac_computername(mac_address, computer_name):
      print(f"INSERT computer {computer_name} with {mac_address} mac address")
  if check_radius_db_mac_exist("radreply", mac_address) == 0:
    results = check_glpi_networkport_has_vlan(networkports_id, mac_address)
    if results:
      for (mac_address, vlan_name, vlan_id) in results:
        insert_radius_radreply_message(mac_address, vlan_id)
        print(f"INSERT vlan: {vlan_id} for {mac_address}")
