"""File for tests"""
import asyncio
from apiSpbStuRuz import ApiSpbStuRuz


async def main():
    async with ApiSpbStuRuz("http://77.247.126.194:3128", timeout=10) as api:
        print(await api.get_teachers())


if __name__ == "__main__":
    asyncio.run(main())
