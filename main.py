"""File for tests"""
import asyncio
from apiSpbStuRuz import ApiSpbStuRuz


async def main():
    async with ApiSpbStuRuz("", timeout=10) as api:
        building = await api.get_building_by_id(11)
        print(building)


if __name__ == "__main__":
    asyncio.run(main())
