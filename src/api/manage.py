# src/app/manage.py

import asyncio
import subprocess
import typer
from sqlalchemy import text

from api.db.session import engine
from api.models import Base
from api.db.seeders import run_all, SEED_FUNCTIONS

app = typer.Typer(help="OpenProvisioner CLI")

@app.command("db-seed")
def db_seed(
    only: str = typer.Option(None, help="Seed específico: users, devices, customers, cpes")
):
    """Popula o banco de dados com dados iniciais (seed)."""
    async def runner():
        if only:
            seed_func = SEED_FUNCTIONS.get(only)
            if seed_func is None:
                typer.echo(f"[ERRO] Seed '{only}' não encontrado. Opções válidas: {', '.join(SEED_FUNCTIONS.keys())}")
                raise typer.Exit(code=1)
            typer.echo(f"Executando seed: {only}")
            await seed_func()
        else:
            typer.echo("Executando todos os seeds...")
            await run_all()
        typer.echo("Seed concluído com sucesso.")

    asyncio.run(runner())

@app.command("db-fresh")
def db_fresh():
    """Dropa todas as tabelas e reaplica as migrations (equivalente ao migrate:fresh)."""
    confirm = typer.confirm("Isso vai DELETAR todas as tabelas e reaplicar as migrations. Continuar?")
    if not confirm:
        typer.echo("Operação cancelada.")
        raise typer.Abort()

    async def reset_db():
        typer.echo("Dropando todas as tabelas...")

        async with engine.begin() as conn:
            await conn.execute(text("DROP SCHEMA public CASCADE"))
            await conn.execute(text("CREATE SCHEMA public"))

        typer.echo("Rodando migrations com Alembic...")
        try:
            subprocess.run(["alembic", "upgrade", "head"], check=True)
            typer.echo("Banco de dados recriado com sucesso via migrations.")
        except subprocess.CalledProcessError:
            typer.echo("[ERRO] Falha ao executar 'alembic upgrade head'")
            raise typer.Exit(code=1)

    asyncio.run(reset_db())

if __name__ == "__main__":
    app()
