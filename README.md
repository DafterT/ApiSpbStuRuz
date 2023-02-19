# Library implementing API
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
## Paths:
* 
## Files:
* **apiSpbStuRuz.py** - this file implements the basic API logic
* **dataClasses.py** - this file contains all the data classes into which the received data is converted
* **logConfig.py** - this file contains the settings for the logger
* **apiSpbStuRuzExeptions.py** - this file contains all the exceptions that are thrown during the operation of the application
* **apiPaths.py** - this file stores all the paths that the library uses for requests to the server
___
