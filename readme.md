# stateup

Upload your state.dat automatically.

Ensures that your state.dat has changed before it uploads.

Can be triggered in any way you choose.

### Installation

##### Required

- [Python3](https://www.python.org/downloads/)
    - Verify it is installed by running `python --version` in your command prompt, ensuring it shows version 3 or greater. If not, try `python3 --version`. Whichever is correct should be used for the rest of the installation instructions
    - We will be using `pythonw.exe` so try `locate pythonw` and ensure it is somewhere

##### Instructions

1. Clone the repository using either method below
    - Press _Clone or download_ and then press _Download ZIP_
    - Extract the files into some directory
    or
    - Press _Clone or download_ and copy the URL
    - `git clone <URL>`
1. Open a terminal in the project directory
    - In the project directory hold `Shift` and right click the background
    - Press _Open command window here_ or _Open PowerShell window here_ or whatever is available on your machine
1. Run the command `python -m pip install -r dependencies`
1. Feel free to delete the files `dependencies`, `readme.md`, and `changelog.md` as they are not required to run the program
1. Run the command `python stateup.py` and follow the instructions

#### Setting up stateup to run when you double click it

It is easiest to keep `stateup.py` in your game directory if you want to use it by double clicking it to start it.

It will work regardless of where you put it, if you'll only use it through Task Scheduler (described below) then you will likely want to put it somewhere else.

If when you double click `stateup.py` it does not run the program, follow these instructions:

1. Right click `stateup.py`
1. Select _Open with_
1. Ensure _Always use this app to..._ is checked
1. Select `Python` from the list

Now when you double click `stateup.py` your stats should be uploaded.

#### Setting up stateup to run every so often while your computer is running

You can set up the application as a Windows Task to have it run on a schedule.

1. Open Task Scheduler (comes with Windows)
1. Click Create Task
1. Fill in the options as follows (* means you can put whatever you want)
    - General Tab
        - Name: stateup*
        - Run only when user is logged in
    - Triggers Tab
        - New
            - Begin the task: On a schedule
            - One time: default (now)*
            - Repeat task every: 1 hour*
            - Enabled: yes
    - Actions Tab
        - Action: Start a program
        -  Program/script: C:\Python38\pythonw.exe*
            - pythonw is the no-terminal version of python
            - To find yours, you can try `where pythonw` on your commandline
        - Add arguments: stateup.py
        - Start in: C:\\...\\stateup
            - This must be the exact directory stateup.py is in
            - To get this open the folder in explorer and copy the text at the top
    - Conditions Tab
        - None
    - Settings Tab
        - Allow the task to be run on demand: yes
        - If the task is already running, then the following rule applies: Stop the existing instance
        - All others disabled in this tab

#### My preferred setup

I didn't want to set mine up hourly because I am not using internals that often. What I did instead is in the 'Triggers' Tab, I selected the trigger "On workstation lock". This means when I perform Windows+L to lock my computer it runs, which works great for me.
