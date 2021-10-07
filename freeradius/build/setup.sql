CREATE DATABASE radius default character set utf8mb4;;
#
#  Create default administrator for RADIUS
#
CREATE USER 'radius'@'%' IDENTIFIED BY '2G97w4ajcNZ7kMebpLNmBKL9';

# The server can read any table in SQL
GRANT SELECT ON radius.* TO 'radius'@'%';

# The server can write to the accounting and post-auth logging table.
#
#  i.e.
GRANT ALL on radius.radacct TO 'radius'@'%';
GRANT ALL on radius.radpostauth TO 'radius'@'%';
