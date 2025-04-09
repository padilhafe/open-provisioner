# OpenProvisioner

- Criar o arquivo de .env informando qual o tipo de ambiente
```
ENV=dev
```

- Criar o arquivo .env.ambiente com as configurações
```
# Project Settings
PROJECT_NAME=OpenProvisioner

# Database Config
DB_ENGINE=mariadb
DB_HOST=localhost
DB_PORT=3307
DB_NAME=test_db
DB_USER=test_user
DB_PASSWORD=test_pass
```

- Comando para rodar o projeto:
```
docker compose -f docker-compose.yml --env-file .env.prod up -d
poetry run alembic upgrade head
poetry run uvicorn app.main:app --reload --app-dir src
```

- Comando para subir o banco de dados de teste
```
docker compose -f docker-compose.dev.yml --env-file .env.dev up -d
poetry run alembic upgrade head
```

- Comando para rodar os testes:
```
poetry run pytest
```