# ⚠️ NOT WORKING (Pure API changed)

**Important:** The Pure app has changed its API (checked: 2025-11-07).  
Requests no longer work.  
The tool is currently **broken** until the new protocol is reverse-engineered.

---

# auto-pure
Automation of likes in the Pure dating app.

The script allows you to like everyone by the required filters.  
It stores information about each liked user in the database and does not like them again.  
While the script is running, you cannot use the Pure app on other devices - otherwise your session will be invalidated.

# Usage

## Install:
```
poetry install
```

## Grab auth data:

Go to [https://pure.app/](https://pure.app/), then extract from Local Storage:

* **soulStorage:userId**
* **soulStorage:sessionToken**

## Run:
```
./main.py like soulStorage:userId soulStorage:sessionToken
```

## Oher commands:
* `./main.py search` - search users in the local DB by description
* `./main.py stats` - show some basic stats

# Algorithm

The protocol was originally encoded in a specific way.
If you're interested, check the **calculate_authorization_hash** function.

---

# Current status

* ✅ Repository kept for reference
* 🛑 Functionality broken due to Pure API update
* 💬 Contributions welcome (updated endpoints / auth flow)
