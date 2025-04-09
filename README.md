# OpenProvisioner

- Comando para rodar o projeto:
```
docker compose up -d
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