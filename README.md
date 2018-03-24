Staff Downloader
================

Middleware script that runs to download staff information from the Kumoricon
website, makes corrections, and formats it for import in 
to [KumoReg](https://github.com/kumoregdev/kumoreg).

Information is saved in JSON files to a (configurable) directory that KumoReg will
scan for new files. Staff badge images are saved to a configurable locaiton for KumoReg
to use.

Each time the script runs, the change set number and last run information will be
saved to lastrun.json, and that will be read each time so that only new changes are
downloaded.


Setup
-------------
Download the script:

```
git clone 'https://github.com/kumoregdev/staffdownloader.git'
```

Configuration
-------------
Edit config.py and update any value set to REPLACE_ME


Running
-------------
```
./run.sh
```

If a venv directory does not exist, a Python virtualenv will be created there and 
requirements will be installed.

Typically this would be run on a schedule from Cron or the scheduler of your choice.
An example crontab entry to run every minute is:

```
* * * * * /full/path/to/script/staffdownloader/run.sh

```

Logging
-------------
By default, logs are saved to staff.log in the current directory. This, along with 
the log level, may be configured in config.py

Updating all data
-----------------------
Delete the last run information file (`lastrun.json` by default) and the information
for every staff member will be downloaded next time the script runs

