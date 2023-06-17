# auto-pure
Automation of likes in dating pure app.
The script allows you to like everyone by the necessary filter.
The script saves the information about the like in the database, does not put the likes again.
When the script is running, you cannot use the app on other devices, otherwise authorization will be canceled.

# Usage

## Install:
```
poetry install
```

## Grab auth data:

go to https://pure.app/, then get from local storage **soulStorage:userId** and **soulStorage:sessionToken**.

## Run:
```
 **soulStorage:userId** *soulStorage:sessionToken**
```

## Oher commands:
* `./main.py search` - search users in local db by description
* `./main.py stats` - some stats

# Algorithm

The protocol is encoded in a special way, if you are interested, then see **calculate_authorization_hash** function.
