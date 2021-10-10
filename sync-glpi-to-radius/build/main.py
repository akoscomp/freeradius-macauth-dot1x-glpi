import time
from datetime import datetime

from config import *
from functions import *

now = datetime.now()

print(now, " - Hello, I'm GLPI and Radius DB sync!")

# Copy data
for (device_name, mac_address, networkports_id) in select_glpi_device_by_mac():
  #print(f"Check mac: {mac_address}")

  # Check if mac address exists in radius auth table
  if (check_radius_db_mac_exist("radcheck", mac_address) == 0):
    if insert_radius_mac_computername(mac_address, device_name):
      print(f"INSERT computer {device_name} with {mac_address} mac address")

  # Check if mac address exists in radius reply table
  if (check_radius_db_mac_exist("radreply", mac_address) == 0):
    results = check_glpi_networkport_has_vlan(networkports_id, mac_address)
    if results:
      for (mac_address, vlan_name, vlan_id) in results:
        insert_radius_radreply_message(mac_address, vlan_id)
        print(f"INSERT vlan: {vlan_id} for {mac_address}")

  # Check if the vlan was removed from glpi, remove it from radius
  elif (not check_glpi_networkport_has_vlan(networkports_id, mac_address)):
    results = check_glpi_networkport_has_vlan(networkports_id, mac_address)
    delete_mac_radius_reply(mac_address)
    print(f"DELETE mac address from reply table: {mac_address}")

  # Check if the vlan id from glpi is the same with radius, if not, update it
  else:
    results = check_glpi_networkport_has_vlan(networkports_id, mac_address)
    if results:
      for (mac_address, vlan_name, vlan_id) in results:
        radius_vlan_id = check_radius_reply_vlan_id(mac_address)
        if (int(radius_vlan_id) != int(vlan_id)):
          update_radius_radreply_vlan_id(mac_address, vlan_id)
          print(f"UPDATE vlan_id in radius tables for mac: {mac_address}, from vlan: {radius_vlan_id} to vlan: {vlan_id}")
