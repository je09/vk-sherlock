# VK-sherlock

### A CLI util intented to make using of VK API to find people easier

This script may be **unstable** for now

## How to install it?

You can clone this repository with:

```bash
git clone https://github.com/je09/vk-sherlock.git
```

Change directory to vk-sherlock with:

```bash
cd vk-sherlock
```

And build it with your version of pip like so (python 3.5 and higher):

```bash
pip install .  # May require pip3 instead of pip
```

## How to use?

To use this script you need to have a VK-account. After the first launch you'll have to enter your login and password. This script uses [vk_api](https://github.com/python273/vk_api) library to interact with VK's API, so every login/password'll be stealed by it's creator, not me. Probably.

**Warning!** This script creates a "**.vk-sherlock**" folder in your home directory and places a config with auth data in there. Remeber to clean it up if you need to.

## Comands avaliable:

| Command           | Description                                  |
| ----------------- | -------------------------------------------- |
| db                | Get id's of objects for searching from VK db |
| friends           | Get user's friends                           |
| geotags           | Get list of photos by geo tags               |
| group-subscribers | Get subscribers of a group                   |
| groups            | Get user's groups                            |
| search            | Search for user by provided criteria         |
| user-info         | Get user's profile info                      |

More information about commands and their options you may find using "--help" command, for example:

```bash
vk-sherlock search --help
Usage: vk-sherlock search [OPTIONS]

  Search for a user by provided criteria

Options:
  --name TEXT                Group name
  --info INTEGER RANGE       1 - basic, 2 - medium, 3 - full
  -c, --count INTEGER RANGE  Number of user's to return
  --city TEXT                City ID
  --country TEXT             Country ID
  --hometown TEXT            Hometown ID
  --university TEXT          University ID
  --sex INTEGER RANGE        1 — female, 2 — male, 0 — any (default)
  --status INTEGER RANGE     1 — Not married, 2 — In a relationship, 3 —
                             Engaged, 4 — Married, 5 — It's complicated, 6 —
                             Actively searching, 7 — In love

  --age_from INTEGER         Minimum age
  --age_to INTEGER           Maximum age
  --birth_day TEXT           Day of birth
  --birth_month TEXT         Month of birth
  --birth_year TEXT          Year of birth
  --work TEXT                Name of the company where users work
  --religion TEXT            User's religious affiliation
  --has_photo                Show users with photo only
  --online                   Show online users only
  --help                     Show this message and exit.
```

### ToDo:

1. Fix missspellings
2. Fix several bugs
3. Add multithreading when it's possible
4. Flag to download images of profile
5. Improve output file structure
6. Add Google Dorks support for working around private profiles
