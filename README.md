Endomondo all history export
================

Export a user's all endomondo history using gpx format. Program generates json file with all user and all workouts description. Name of json file is endomondo technical user id like 898773.json. For each workout gpx file is saved in local directory with the name of technical workout id like 23513251325.gpx 


Usage
-----

The script  may be used to backup the complete workout history:

    python export.py -u user_email -p user_password

usage: export.py [-h] [-v] [-u USER] [-p PASSWORD]

Endomondo data export

optional arguments:
  -h, --help   show this help message and exit
  -v           Increase verbosity (logs all data going through) (default:
               False)
  -u USER      Endomondo user (default: None)
  -p PASSWORD  Endomondo password (default: None)


Requirements
------------

- Python 3.6+
    - requests


Installing
----------

Install the requirements (using virtual env) :

    pip install -r requirements


Author
-------

[@mikspec](https://github.com/mikspec)
