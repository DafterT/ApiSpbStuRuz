# Library implementing API

___
<p align="center">
<a href="https://pypi.org/project/ApiSpbStuRuz/">
    <img src="https://img.shields.io/badge/download-PyPi-red.svg">
</a>
<img src="https://img.shields.io/badge/made%20by-Dafter-orange.svg">
<img src="https://img.shields.io/github/license/DafterT/ApiSpbStuRuz">
<img src="https://img.shields.io/github/last-commit/DafterT/ApiSpbStuRuz">
</p>

___

## How to use:

You are required to create an `ApiSpbStuRuz` using `async with` statement. For example like this:

```Python
import asyncio
import ApiSpbStuRuz


async def main():
    async with ApiSpbStuRuz.ApiSpbStuRuz() as api:
        teacher = await api.get_teacher_by_id(999335)
        print(teacher)


if __name__ == "__main__":
    asyncio.run(main())
```

When you create a class, you have a number of parameters:

* **create_logger** - if you want to use a logger, pass True, otherwise don't change.
* **path_log** - the path to the folder where the logger will write logs.  
  Before using, do not forget to enable the logger.
* **try_create_dict** - If you want the logger not to try to create a folder with logs,
  then turn off this parameter.
* **proxy** - If you want to use a proxy for requests, then pass them to this parameter.  
  Proxies are not used as standard. The proxy should be transmitted in the format required by the aiohttp library
* **timeout** - If you want to change the request timeout from 5 seconds, then use this parameter

___

## Functions:

* `get_faculties` - returns a list of faculties
* `get_faculty_by_id` - gets the id of the faculty, returns an object with the faculty
* `get_groups_on_faculties_by_id` - gets the faculty number, returns a list of groups in this faculty
* `get_teachers` - returns a list of teachers (can take a long time to run because there is a lot of data)
* `get_teacher_by_id` - returns the teacher by his id (not oid)
* `get_teacher_scheduler_by_id` - returns the teacher's schedule by its id (not oid)
* `get_teacher_scheduler_by_id_and_date` - returns the teacher's schedule by its id (not oid) on a specific
  date (actually returns the schedule for the week on which this date is)
* `get_buildings` - returns a list of buildings
* `get_building_by_id` - returns a building by its id
* `get_rooms_by_building_id` - returns rooms in a building by its id
* `get_rooms_scheduler_by_id_and_building_id` - returns the schedule of the room by its id in the building by its id
* `get_rooms_scheduler_by_id_and_building_id_and_date` - returns the schedule of the room by its id in the building by
  its id on a certain date (actually returns the schedule for the week on which this date is)
* `get_groups_scheduler_by_id` - returns the group schedule by its id
* `get_groups_scheduler_by_id_and_date` - returns the group schedule by its id by date
  (actually returns the schedule for the week on which this date is)
* `get_groups_by_name` - returns a group object by its name (сan return multiple objects)
* `get_teachers_by_name` - returns a teacher object by her name (сan return multiple objects)
* `get_rooms_by_name` - returns a room object by its name (сan return multiple objects)

___

## Paths:

* **https://ruz.spbstu.ru/api/v1/ruz**
    * **/faculties** - getting a list of faculties (institutes)
        * **/id** - getting the name by the id of the department (institute)
            * **/groups** - getting a list of groups by department (institute) id
    * **/teachers** - list of all teachers
        * **/id** - search for a teacher by id
            * **/scheduler** - teacher's schedule by his id for the current week
                * **?date=yyyy-mm-dd** - teacher's schedule by his id for the week with the entered date
    * **/buildings** - list of "structures"/buildings (Note that it has a bunch of garbage values)
        * **/id** - search for "structures" by id
            * **/rooms** - list of rooms in a building by its id
                * **/id/scheduler** - schedule by room's id
                    * **?date=yyyy-mm-dd** - similarly by date
    * **/scheduler/id** - getting a schedule by group id for the current week
        * **?date=yyyy-mm-dd** - getting a week by a specific date
    * **/search**
        * **/groups?q=name** - search for a group by its name (example name="3530901/10001" -> 35376)
        * **/teachers?q=name** - search for a teacher by first name/last name/patronymic/full_name (replace spaces with
          %20 when requested)
        * **/rooms?q=name** - search by audience name

___

## Files:

* **apiSpbStuRuz.py** - this file implements the basic API logic
* **dataClasses.py** - this file contains all the data classes into which the received data is converted
* **logConfig.py** - this file contains the settings for the logger
* **apiSpbStuRuzExeptions.py** - this file contains all the exceptions that are thrown during the operation of the
  application
* **apiPaths.py** - this file stores all the paths that the library uses for requests to the server

___
