"""File for tests"""
import asyncio
from apiSpbStuRuz import ApiSpbStuRuz


async def main():
    async with ApiSpbStuRuz("", timeout=10) as api:
        buildings = await api.get_buildings()
        print(buildings)


if __name__ == "__main__":
    asyncio.run(main())
