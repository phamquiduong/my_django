## Python packages and environment
### Use Pip and Venv
> Create environment
> ```bash
> python -m venv .venv
> ```

> Active environment
> ```bash
> .\.venv\Scripts\activate
> ```

> [!NOTE]
> If you encounter an activation error, open **PowerShell as Administrator** and run:
> ```bash
> Set-ExecutionPolicy Unrestricted -Force
> ```

> Install packages
> ```bash
> pip install -r requirements.txt
> ```

### Use Poetry
> Install poetry
> ```bash
> pip install poetry
> ```

> Install packages
> ```bash
> poetry install
> ```

> Add new package
> ```bash
> poetry add <package_name>
> ```

> Active environment
> ```bash
> Invoke-Expression (poetry env activate)
> ```

<br>

## Run by Docker
### Software
- All systems: [Docker Desktop](https://www.docker.com/)
- In MacOS: [OrbStack](https://orbstack.dev/)

### Some command
> Run by script
> ```bash
> .\scripts\run_docker.bat
> ```

> Start all docker-compose services
> ```bash
> docker-compose --profile * up --build -d
> ```
> **List profiles:** `server` `database` `mail_server` `celery_worker` `monitor` `db_ui`

> Turn off all docker-compose services
> ```bash
> docker-compose --profile * down
> ```

<br>

## Run manual
### Software
- Install [PostgreSQL 17.6](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
- Install [Redis for Windows](https://github.com/tporadowski/redis/releases)
- Install [DynamoDB Local](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html) (required [JDK](https://www.oracle.com/asean/java/technologies/downloads/))
  > ```bash
  > java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
  > ```

### Environment config
- Copy `.env.example` file to `.env` in **root folder**
- Setup the `Database`, `Caches` & `Celery` and `DynamoDB`

### Server command
> Run by script
> ```bash
> .\scripts\run_manual.bat
> ```

> Run server
> ```bash
> python manage.py runserver 0.0.0.0:80
> ```

> Run migrate
> ```bash
> python manage.py migrate
> ```

> Run wait for the database
> ```bash
> python manage.py wait_for_db
> ```

> Run wait for the Redis
> ```bash
> python manage.py wait_for_redis
> ```

> Run Celery send mail worker
> ```bash
> celery -A main worker -n email@%h -l INFO -Q email
> ```

<br>

## Note
> You should install stubs for "upgrade" the Pylance in VScode
> ```bash
> pip install django-stubs djangorestframework-stubs
> ```

<br>

## Reference
- [The VietNam provinces database](https://github.com/thanglequoc/vietnamese-provinces-database)
