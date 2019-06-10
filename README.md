# django-apache-logs

## Run with docker-compose
### Envs (Step 1)
```
cp conf/.env-example conf/.env
cp devops/.env-example devops/.env
```

### Start up server (Step 2)
```
cd devops && docker-compose -p django-apache-logs up
```

## Run development server
### Envs (Step 1)
```
cp conf/.env-example conf/.env
cp devops/.env-example devops/.env
```

Change env vars in conf/.env
```
POSTGRES_DB_HOST=localhost
POSTGRES_DB_PORT=54321
```

### Virtualenv and dependencies (Step 2)
```
pipenv shell --python python3.7
pipenv install # in virtualenv
```

### Start up postgres (Step 3)
```
cd devops && docker-compose -p django-apache-logs up postgres
```

### Start up postgres (Step 3)
```
python manage.py runserver
```

## Connect to docker container
```
docker exec -it django-apache-logs_app_1 sh
```

## Run download script
```
python manage.py download -su http://www.almhuette-raith.at/apache-log/access.log
```

## Fixtures 
```
python manage.py dumpdata logger.log > apps/logger/fixtures/log.json 
python manage.py loaddata apps/logger/fixtures/log.json
```
