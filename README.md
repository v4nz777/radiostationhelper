# PROJECT STATION

### A simple project to make life in radio station easier.
### Also includes office tasks...

---

## How To Start

- Install Python
- Install virtual environment: *pip install virtualenv* | ***this is optional***
- Install *requirements.txt*
- Setup machine's ipv4 to static, then take note of the set IP
- Change the **old ip** to the **set ip** in files:  *runserver.py*, *settings.py* and inside nginx's config file
- Then run *python runserver.py*


## OSError Quickfix

- Open Powershell as admin
- Run *Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted*

## Other Reminders
- Setup your own database
- Setup SSL of your static ip to computer