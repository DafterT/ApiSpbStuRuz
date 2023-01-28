"""File for tests"""
import asyncio
from apiSpbStuRuz import ApiSpbStuRuz
from apiPaths import *


async def main():
    async with ApiSpbStuRuz() as api:
        print(await api.get_response_json(faculties_list))


if __name__ == "__main__":
    asyncio.run(main())
