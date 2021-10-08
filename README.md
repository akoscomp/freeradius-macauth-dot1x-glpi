# freeradius-macauth-dot1x-glpi
FreeRADIUS server tested on Mikrotik switches, uses GLPI-Project as MAC and VLAN source, exposed by traefik proxy.

I want to make a network authentication service that can authenticate computers with mac address or with 802.1x. For this I want to use GLPI as source, because GLPI can store the computers mac address and vlan information.

The bottleneck of this project is the synchronization between glpi database and radius database. I try to solve it with a python script.

# Usage
Rename .env.sample to .env and configure it

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

## Passwords that need to be changed
 - each_folder/.env
 - freeradius/build/setup.sql - same with MYSQL_RADIUS_PASSWORD
 - freeradius/build/config/mods-enabled/sql - same with MYSQL_RADIUS_PASSWORD
 - freeradius/build/config/clients.conf - change password for client connections
