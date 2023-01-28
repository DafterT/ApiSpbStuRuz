"""File for tests"""
import asyncio
from apiSpbStuRuz import ApiSpbStuRuz


async def main():
    async with ApiSpbStuRuz() as api:
        await api.get_response()


if __name__ == "__main__":
    asyncio.run(main())
