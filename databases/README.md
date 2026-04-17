## sqlite
install 
```bash
pip install sqlalchemy 
pip install greenlet
```
or all-at-once
```bash
pip install "sqlalchemy[asyncio]"
```
and install async database driver
```bash
pip install sqlalchemy aiosqlite
```

use connection string (for sqlalchemy):
```python
DATABASE_URL = "sqlite+aiosqlite:///movies.db" 
```

run script to create table 'movies':
```bash
python example.py
```
sqlite db file will be created automatically - `movies.db`
we can inspect created tables:
```bash
% sqlite3 movies.db
sqlite> .tables
movies
sqlite> select * from movies;
1|Inception|Christopher Nolan|2010
2|The Matrix|The Wachowskis|1999
3|Interstellar|Christopher Nolan|2014
sqlite> .quit
```


## for postgres
Run postgresql database in docker:
```bash
docker run -d -p 6500:5432 \
	--name postgres \
	-e POSTGRES_PASSWORD=admin \
	-e PGDATA=/var/lib/postgresql/data/pgdata \
	-v /Users/irynamitina/tmp/pgdata:/var/lib/postgresql/data \
	postgres
```
Default user `postgres` (password='admin') and default database `postgres` will be created.

For PostgreSQL, the database "movies_db" must already exist before create_all() runs. 
create_all() creates tables, not the database itself.
To create database: 'movies_db' use `psql` CLI:
```bash
$ docker exec -it postgres psql -U postgres
postgres=# create database movies_db;
CREATE DATABASE
postgres=# \c movies_db;
You are now connected to database "movies_db" as user "postgres".
movies_db=# 
```


install async database driver
```bash
pip install sqlalchemy asyncpg
```
and use connection string
```python
DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost:6500/movies_db" 
```

and run script to create table movies;
```bash
python example.py
```
check table was created with psql:
```bash
movies_db=# \dt
         List of relations
 Schema |  Name  | Type  |  Owner   
--------+--------+-------+----------
 public | movies | table | postgres
(1 row)

movies_db=# select * from movies;
 id |    title     |     director      | year 
----+--------------+-------------------+------
  1 | Inception    | Christopher Nolan | 2010
  2 | The Matrix   | The Wachowskis    | 1999
  3 | Interstellar | Christopher Nolan | 2014
(3 rows)

movies_db=# \quit
```

## mysql
install async database driver
```bash
pip install sqlalchemy aiomysql
```


