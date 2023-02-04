"""File for tests"""
import asyncio
from apiSpbStuRuz import ApiSpbStuRuz


async def main():
    async with ApiSpbStuRuz("", timeout=10) as api:
        groups = await api.get_groups_by_name("3530901/1")
        [print(group) for group in groups]


if __name__ == "__main__":
    asyncio.run(main())
