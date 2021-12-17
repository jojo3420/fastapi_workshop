# create a container
$ docker run --name fastapi-db \
-p 3306:3306 \
-e MYSQL_ROOT_PASSWORD=dkagh12#$ \
-e MYSQL_USER=root \
-e MYSQL_PASSWORD=dkagh12#$ \
-d mysql:8.0 \
--character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci

# check
#$ docker exec -it fastapi-db mysql -uroot -p