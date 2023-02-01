"""File for tests"""
import asyncio
from apiSpbStuRuz import ApiSpbStuRuz


async def main():
    async with ApiSpbStuRuz("", timeout=10) as api:
        print(await api.get_teacher_by_id(99870))


if __name__ == "__main__":
    asyncio.run(main())
