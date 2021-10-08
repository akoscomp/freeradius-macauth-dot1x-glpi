GLPI_VERSION=9.5.6
DATA_FOLDER=../data
MARIADB_HOST=lan-db-mariadb

MYSQL_ROOT_PASSWORD=$(grep MYSQL_ROOT_PASSWORD .env | xargs)
MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD#*=}

PROXY_NETWORK=$(grep PROXY_NETWORK .env | xargs)
PROXY_NETWORK=${PROXY_NETWORK#*=}

echo "create data folders"
mkdir -p $DATA_FOLDER
mkdir -p $DATA_FOLDER/traefik
mkdir -p $DATA_FOLDER/freeradius/logs

FILE=${DATA_FOLDER}/traefik/acme.json
if test -f "$FILE"; then
  echo "$FILE exist"
else
  echo "{}" > $FILE
  chmod 600 $FILE
fi

docker network create ${PROXY_NETWORK}
docker network create mariadb

docker-compose up -d

echo "wait 10s for database startup ..."
sleep 10

echo "create radius tables"
cat ../freeradius/build/setup.sql | docker exec -i lan-db-mariadb /usr/bin/mysql -u root --password=${MYSQL_ROOT_PASSWORD}
cat ../freeradius/build/schema.sql | docker exec -i lan-db-mariadb /usr/bin/mysql -u root --password=${MYSQL_ROOT_PASSWORD} radius

echo "download glpi"
curl -sSL https://github.com/glpi-project/glpi/releases/download/${GLPI_VERSION}/glpi-${GLPI_VERSION}.tgz --output ../data/glpi.tgz

echo "extract glpi"
tar -xf ${DATA_FOLDER}/glpi.tgz -C ${DATA_FOLDER}

echo "set permissions, need root rights (sudo)"
sudo chown 33:33 -R ${DATA_FOLDER}/glpi/config
sudo chown 33:33 -R ${DATA_FOLDER}/glpi/files
sudo chown 101:101 ${DATA_FOLDER}/freeradius/logs

echo "Done"
