"""File for tests"""
import asyncio
from apiSpbStuRuz import ApiSpbStuRuz


async def main():
    async with ApiSpbStuRuz("", timeout=10) as api:
        teachers = await api.get_teachers_by_name("")
        [print(teacher) for teacher in teachers]


if __name__ == "__main__":
    asyncio.run(main())
