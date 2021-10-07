# freeradius-mikrotik-glpi
FreeRADIUS server tested on Mikrotik switches, uses GLPI-Project as MAC and VLAN source

## Initialize, start database and docker :

```
cd mariadb
./init.sh
```

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
Can test with command: `radtest aa:bb:cc:dd:ee:ff aa:bb:cc:dd:ee:ff localhost 0 wNgb9tzajFBjAv6W9NFXGWmp`

### Start glpi
```
cd glpi
docker-compose up -d
```
GLPI configuration parameters is in `mariadb/.env` file
