# freeradius-macauth-dot1x-glpi
FreeRADIUS server tested on Mikrotik switches, uses GLPI-Project as MAC and VLAN source

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
