"""File for tests"""
import asyncio
from apiSpbStuRuz import ApiSpbStuRuz


async def main():
    async with ApiSpbStuRuz("", timeout=10) as api:
        rooms = await api.get_rooms_by_name("201")
        [print(room) for room in rooms]


if __name__ == "__main__":
    asyncio.run(main())
