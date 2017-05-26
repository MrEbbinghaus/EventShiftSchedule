# EventShiftSchedule

This is a Django app to provide a simple shift schedule. E.g. for partys!
you _need_ to place this inside your Django project folder and configure it correctly!

## Installation
1.  Change to your Django project folder.
2.  If your project is in a git repository: `git submodule add https://github.com/MrOerni/EventShiftSchedule`. If not. Just clone it!
3.  Add `EventShiftSchedule` to your `INSTALLED_APPS` in `settings.py`.
4.  Add an url to `url.py`. E.g.: `url(r'^ess/', include("EventShiftSchedule.urls", namespace='EventShiftSchedule'))`.
5.  Install the requirements with `pip install -r requirements.txt`. Tipp: If you have a requirements file in your project folder, just add `-r EventShiftSchedule/requirements.txt` to it!
6.  `makemigrations`, `migrate` as usual.

## Create an event
1. Go into the admin menu. (e.g. `localhost:1234/admin/`)
2. Add an `Event`. You have to enter at least a date.
3. Add some Positions. (e.g. "Bar", "Security", ...) whatever Positions you want on your Party. You have to enter a Name, a prefered number of users which can take this position per timeslot, and the event from 2.
4. Add some Times. These are timeslots. Add the date (remember to use the next date vor timeslots past midnight), the start time, the duration of this slot and the event from 2. You may enter an alternative Name for your Slot.
5. Done! Visit `/ess` to show a list of events. Your new event should be there. Click it!

## Create one-time positions (e.g. preparation, tidy up afterwards)
1. Create an event like in the chapter above.
2. Add an onetimeposition, you have to set a name, a time and the event you just created.

## Contact

You can contact me under bjoern@ebbinghaus.me
