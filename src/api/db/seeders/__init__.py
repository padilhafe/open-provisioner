from api.db.seeders.user_seeder import seed_users
from api.db.seeders.device_seeder import seed_devices
from api.db.seeders.customer_seeder import seed_customers
from api.db.seeders.cpe_seeder import seed_cpes
from api.db.session import async_session

SEED_FUNCTIONS = {
    "users": seed_users,
    "devices": seed_devices,
    "customers": seed_customers,
    "cpes": seed_cpes,
}

async def run_all():
    async with async_session() as session:
        await seed_users(session)
        await seed_devices(session)
        await seed_customers(session)
        await seed_cpes(session)
