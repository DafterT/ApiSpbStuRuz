"""File for tests"""
import asyncio
from apiSpbStuRuz import ApiSpbStuRuz


async def main():
    async with ApiSpbStuRuz("http://77.247.126.194:3128") as api:
        faculties = await api.get_faculties()
        print(faculties)
        if faculties is None:
            return
        tasks = []
        for item in faculties:
            # print(await api.get_faculty_by_id(item.id))
            tasks.append(asyncio.create_task(api.get_faculty_by_id(item.id)))
        for task in tasks:
            print(await task)


if __name__ == "__main__":
    asyncio.run(main())
