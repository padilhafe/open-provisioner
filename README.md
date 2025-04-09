# OpenProvisioner

- Comando para rodar o projeto:
```
docker compose up -d
poetry run alembic upgrade head
poetry run uvicorn app.main:app --reload --app-dir src
```

- Comando para subir o banco de dados de teste
```
docker compose -f docker-compose.test.yml --env-file .env.test up -d
poetry run alembic upgrade head
```

- Comando para rodar os testes:
```
poetry run pytest
```