## Some script with Docker compose
#### Run all services
```
.\scripts\run_docker.bat
```

<br>

## Run manual (without Docker)
#### Software
- Install PostgreSQL 17.6: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
- Install Redis for Windows: https://github.com/tporadowski/redis/releases

#### Environment config
- Copy `docker/.env.example` file to `.env` in **root folder**
- Change `POSTGRES_HOST` and `REDIS_HOST` value to `localhost`

#### Run Django server
```
.\scripts\run_manual.bat
```

<br>

## Reference
- [The VietNam provinces database](https://github.com/thanglequoc/vietnamese-provinces-database)
