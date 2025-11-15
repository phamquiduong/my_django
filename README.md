## Some script with Docker compose
#### Run all services
```bash
.\scripts\run_docker.bat
```

<br>

## Run manual (without Docker)
#### Software
- Install [PostgreSQL 17.6](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
- Install [Redis for Windows](https://github.com/tporadowski/redis/releases)
- Install [DynamoDB Local](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html) (required [JDK](https://www.oracle.com/asean/java/technologies/downloads/))
    > ```bash
    > java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
    > ```

#### Environment config
- Copy `.env.example` file to `.env` in **root folder**
- Set the `Database`, `Caches` & `Celery` and `DynamoDB`

#### Run Django server
```bash
.\scripts\run_manual.bat
```

#### Run Celery send mail worker
```bash
celery -A main worker -n email@%h -l INFO -Q email
```

<br>

## Reference
- [The VietNam provinces database](https://github.com/thanglequoc/vietnamese-provinces-database)
