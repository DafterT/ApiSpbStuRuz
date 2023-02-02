"""File for tests"""
import asyncio
from apiSpbStuRuz import ApiSpbStuRuz


async def main():
    async with ApiSpbStuRuz("", timeout=10) as api:
        teachers_scheduler = await api.get_teacher_scheduler_by_id(3810)
        print(teachers_scheduler)


if __name__ == "__main__":
    asyncio.run(main())
