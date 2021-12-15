# create a container
$ docker run --name fastapi-db \
-p 3306:3306 \
-e MYSQL_ROOT_PASSWORD=1234 \
-e MYSQL_USER=admin \
-e MYSQL_PASSWORD=1234 \
-d mysql:8.0 \
--character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci

# check
#$ docker exec -it fastapi-db mysql -uroot -p