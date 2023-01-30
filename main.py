"""File for tests"""
import asyncio
from apiSpbStuRuz import ApiSpbStuRuz


async def main():
    async with ApiSpbStuRuz() as api:
        faculties = await api.get_faculties()
        for item in faculties:
            print(await api.get_faculty_by_id(item.id))


if __name__ == "__main__":
    asyncio.run(main())
