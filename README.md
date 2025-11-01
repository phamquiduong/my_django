## Some script with Docker compose
#### Run all services
```
.\scripts\docker\run_all.bat
```

#### Run only PostgreSQL
```
.\scripts\docker\run_only_postgresql.bat
```

#### Create Django super user
```
.\scripts\docker\create_superuser.bat
```

#### Refresh location data into DB
```
.\scripts\docker\refresh_location.bat
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
.\scripts\run_django.bat
```

<br>

## Reference
- Thank you so much. The VietNam provinces database: https://github.com/thanglequoc/vietnamese-provinces-database
