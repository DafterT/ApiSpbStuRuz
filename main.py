"""File for tests"""
import asyncio
from apiSpbStuRuz import ApiSpbStuRuz


async def main():
    async with ApiSpbStuRuz("", timeout=10) as api:
        rooms_scheduler = await api.get_rooms_scheduler_by_id_and_building_id_and_date(11, 547, 2023, 2, 10)
        print(rooms_scheduler)


if __name__ == "__main__":
    asyncio.run(main())
