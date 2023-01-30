"""File for tests"""
import asyncio
from apiSpbStuRuz import ApiSpbStuRuz


async def main():
    async with ApiSpbStuRuz() as api:
        print(await api.get_faculties())


if __name__ == "__main__":
    asyncio.run(main())
