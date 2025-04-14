# OpenProvisioner

- O projeto precisa do pacote poetry instalado no sistema.

- Criar o arquivo de .env informando qual o tipo de ambiente
```
ENV=prod
```

- Criar o arquivo .env.ambiente com as configurações
```
# .env.prod

# Project Settings
PROJECT_NAME=OpenProvisioner

# Database Config
DB_ENGINE=mariadb
DB_HOST=localhost
DB_PORT=3307
DB_NAME=openprovisioner_db
DB_USER=dbuser
DB_PASSWORD=dbpass
```

- Comando para rodar o projeto:
```
poetry install
docker compose -f docker-compose.yml --env-file .env.prod up -d
poetry run alembic upgrade head
poetry run python src/api/manage.py db-seed
poetry run uvicorn api.main:app --reload --app-dir src
```

- Para limpar o ambiente
```
docker compose -f docker-compose.yml --env-file .env.prod down
docker volume rm open-provisioner_postgres_data
```

- Comando para rodar os testes:
```
poetry run pytest
```

- Comando para gerar nova migration
```
poetry run alembic revision --autogenerate -m "create TABLE table"
```