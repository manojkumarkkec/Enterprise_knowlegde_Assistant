import asyncio

from app.shared.database.session import AsyncSessionLocal
from app.auth.security.rbac import seed_rbac


async def main():

    async with AsyncSessionLocal() as session:

        await seed_rbac(session)


if __name__ == "__main__":

    asyncio.run(main())