from git_base import *
from random import randint
from datetime import datetime
from sys import exit as sys_exit
import traceback

schedule_template = '''name: "Daily Fudan"

on:
  schedule: # scheduled at (UTC+8) everyday
    - cron: "%s"
    - cron: "%s"
  workflow_dispatch:

env:
  RUN_ENV: 'prod'
  TZ: 'Asia/Shanghai'
  FUCK_GH_PAT: ${{ secrets.GH_PAT }}
  
jobs:
  build:
    runs-on: ubuntu-latest
    # if: github.ref == 'refs/heads/master'

    steps:
      - name: Checkout master with GH_PAT
        if: ${{ env.FUCK_GH_PAT }}
        uses: actions/checkout@v2
        with:
          fetch-depth: 2
          ref: main
          token: ${{ secrets.GH_PAT }}

      - name: Checkout master without GH_PAT
        if: ${{ !env.FUCK_GH_PAT }}
        uses: actions/checkout@v2
        with:
          fetch-depth: 0
          ref: main

      - name: Set up python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9

      - name: edit_actions.py
        if: ${{ env.FUCK_GH_PAT }}
        run: python3 ./edit_actions.py '${{ secrets.SCHEDULE }}'

      - name: run.py
        run: python3 ./run.py '${{ secrets.FUDAN }}'
'''

am_inf=19
am_sup=22
pm_inf = 5
pm_sup = 8
t_inf = 4
t_sup = 15

def getRandCron_am():
    mins = randint(0,59)
    hours = randint(am_inf,am_sup) % 24
    return f'{mins} {hours} * * *'

def getRandCron_pm():
    mins = randint(0,59)
    hours = randint(pm_inf,pm_sup) % 24
    return f'{mins} {hours} * * *'

def is_pm():
    uctnow = datetime.utcnow()
    uctnow = uctnow.hour
    if uctnow < t_inf:
        uctnow += 24
    return t_inf < uctnow < t_sup
    
def get_schedule():
    return schedule_template%(getRandCron_am(),getRandCron_pm())

GMT_FORMAT = 'Date:   %a %b %d %H:%M:%S %Y +0800'
def is_today_created(val):
    date = val.split('\n')[2]
    date = datetime.strptime(date, GMT_FORMAT)
    date = (datetime.now()-date).total_seconds()//3600
    print('timedelta', date)
    return date <= 12

def is_autocreated():
    ret, val = subprocess.getstatusoutput("git log -1")
    if ret:
        print(ret, val)
        return False
    if 'autocreated by git_base.py' in val:
        if is_today_created(val):
            sys_exit(0)
        return True
    return False

def update_schedule():
    with open(r'./.github/workflows/main.yml','w',encoding='utf-8') as f:
        f.write(get_schedule())

def get_my_arg():
    print('Please get token from https://github.com/settings/tokens')
    arg = get_arg()
    if not arg:
        print('use default SCHEDULE')
        return
    SCHEDULE = arg
    global am_inf, am_sup, pm_inf, pm_sup, t_inf, t_sup
    if len(SCHEDULE) == 6:
        am_inf = int(SCHEDULE[0])
        am_sup = int(SCHEDULE[1])
        pm_inf = int(SCHEDULE[2])
        pm_sup = int(SCHEDULE[3])
        t_inf = int(SCHEDULE[4])
        t_sup = int(SCHEDULE[5])
    else:
        print('wrong SCHEDULE. use default SCHEDULE')
    print(am_inf, am_sup, pm_inf, pm_sup, t_inf, t_sup)

def main():
    if is_autocreated():
        if git_revoke():
            return
    update_schedule()
    git_push()

try:
    get_my_arg()
except:
    print(traceback.format_exc())

if is_pm():
    try:
        main()
    except SystemExit:
        pass
    except:
        print(traceback.format_exc())
