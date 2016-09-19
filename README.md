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
