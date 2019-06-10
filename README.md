# django-apache-logs

## Feature list
- [x] Management command с прогрессбаром
- [x] Фронтенд пагинация, поиск
- [x] Количество уникальных IP
- [x] Top 10 самых распространенных IP адресов, в формате таблички где указан IP адрес и количество его вхождений
- [x] Количество GET, POST, ... (http методов)
- [x] Общее кол-во переданных байт (суммарное значение по полю "размер ответа")
- [x] Хорошее оформление и комментирование кода (не излишнее, но хорошее);
- [x] Оформление frontend части;
- [x] Упаковка проекта в docker/docker-compose;
- [x] Оптимизация запросов к БД;
- [x] Кнопка экспорта данных на таблице с результатами, при нажатии на которую будет скачиваться файлик в формате XLSX с результатами выдачи;

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

### Start server (Step 4)
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
