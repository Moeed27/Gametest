# REMOVE THIS FILE BEFORE SUBMISSION

## SETUP

Its set it up for python 3.12, hopefully that shouldn't cause any major problems.

Create your .venv via your IDE and type in the command `pip install -r requirements.txt` in terminal

Run app.py to start the app and it should hopefully work!

## DATABASE SETUP

- Download .env and server.key from [This Folder](https://drive.google.com/drive/folders/15xkscblsnj-faE75lzxFW5yYVLM3qLEM?usp=drive_link)
  - Place these in your project root file
  - Do **NOT** add these to git - these should be ignored
- When running, the server should connect to the database via ssh tunnel
- If any issues arise, speak to Isaac and show him the error

## TESTING SETUP

- From command line, run `source .venv/bin/activate` (MacOS) or `./.venv/Scripts/Activate.ps1` (Windows PowerShell)
- run `pytest` to run all tests
  - please see [pytest documentation](https://docs.pytest.org/en/stable/index.html) for any arguments you might want
- after tests have run/failed, run `deactivate` to leave .venv

