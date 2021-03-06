# freeradius-macauth-dot1x-glpi
[FreeRADIUS](https://freeradius.org/) server tested on [Mikrotik](https://mikrotik.com/) switches (probably will work with all switches), uses [GLPI-Project](https://glpi-project.org/) as MAC and VLAN source, web services exposed by [Traefik](https://traefik.io/) proxy.

I want to make a network authentication service that can authenticate computers with mac address or with 802.1x. For this I want to use GLPI as source, because GLPI can store the computers mac address and vlan information.

The bottleneck of this project is the synchronization between glpi database and radius database. I try to solve it with a python script.

# Start and configure services

## Initialize, start database and create docker networks:

```
cd mariadb
./init.sh
```
Update GLPI_VERSION to latest in init.sh

### Start traefik
```
cd traefik
docker-compose up -d
```

### Start freeradius
```
cd freeradius
docker-compose up -d
```
Can test with command: `radtest aa:bb:cc:dd:ee:ff aa:bb:cc:dd:ee:ff localhost 0 radius-password-from-clients-conf`

### Start glpi
```
cd glpi
docker-compose up -d
```
GLPI configuration parameters is in `mariadb/.env` file

### Start sync-glpi-to-radius
```
cd sync-glpi-to-radius
docker-compose up -d
```
This container can sync glpi database with radius database. Can add and remove vlan tags, configured for an interface. The synchronization run periodically, configured in .env. 

## Passwords that need to be changed
 - each_folder/.env
 - freeradius/build/setup.sql - same with MYSQL_RADIUS_PASSWORD
 - freeradius/build/config/mods-enabled/sql - same with MYSQL_RADIUS_PASSWORD
 - freeradius/build/config/clients.conf - change password for client connections
 - sync-glpi-to-radius/build/config.py
