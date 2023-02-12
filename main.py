"""
The file is exclusively for testing implemented functions

Date of create file: 01.28.2023
"""

import asyncio
from apiSpbStuRuz import ApiSpbStuRuz


async def main():
    async with ApiSpbStuRuz("", timeout=10) as api:
        teacher = await api.get_teacher_by_id(9217)
        print(teacher)


if __name__ == "__main__":
    asyncio.run(main())
