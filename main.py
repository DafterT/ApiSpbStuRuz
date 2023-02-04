"""File for tests"""
import asyncio
from apiSpbStuRuz import ApiSpbStuRuz


async def main():
    async with ApiSpbStuRuz("", timeout=10) as api:
        groups_scheduler = await api.get_groups_scheduler_by_id(35376)
        print(groups_scheduler)


if __name__ == "__main__":
    asyncio.run(main())
