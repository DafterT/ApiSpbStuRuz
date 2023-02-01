"""File for tests"""
import asyncio
from apiSpbStuRuz import ApiSpbStuRuz


async def main():
    async with ApiSpbStuRuz("", timeout=10) as api:
        teacher = await api.get_teacher_scheduler_by_id(3810)
        print(teacher.teacher)
        print(type(teacher.days))


if __name__ == "__main__":
    asyncio.run(main())
