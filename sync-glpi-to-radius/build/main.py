import time

from config import *
from functions import *

print("Hello, I'm GLPI and Radius DB sync!")

# Copy data
for (computer_name, mac_address) in select_glpi_mac_computername():
  print(f"Check mac: {mac_address}")
  if check_radius_db_mac_exist(mac_address) == 0:
    if insert_radius_mac_computername(mac_address, computer_name):
      print(f"INSERT computer {computer_name} with {mac_address} mac address")
