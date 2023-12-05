# Instagram Bot

## This is a Python script for automating actions on Instagram, such as sending direct messages, liking and commenting on posts.

### Prerequisites:

- Python 3.x
- Selenium library
- ChromeDriver
- customtkinter

### Installation:

1. Open the code:
   using any IDE or terminal/cmd

2. Install the required dependencies:
   `pip install -r requirements.txt`

### Usage:

1. Fill in the account details and desired actions in the Instagram.py / accounts.json file.

2. Run the script:

      These are the options that you can add in the `python Instagram.py` command:

   - `-h, --help` Show this help message and exit.
   - `-a, --accounts` Use multiple accounts.
   - `-c, --comment` Comment on posts.
   - `-d, --dm` Send direct messages.
   - `-ls, --likestories` Like all current users' stories.
   - `-llp, --likelatestpost` Like users' latest post.
   - `-ht HASHTAG, --hashtag HASHTAG` Hashtag to scrape posts from.
   - `-cm MESSAGE, --commentmessage MESSAGE` Comment or message to post.
   - `-dm MESSAGE, --message MESSAGE` Send direct message to users.
   - `-del DELAY, --delay DELAY` Delay in seconds between actions.

   Example commands:

   - `python Instagram.py -ls` The bot will start to search for users in "users.json" file and will like all available stories of each of them. The delay time between each user is 5 seconds (default 5 secs if not specified).

   - `python Instagram.py -d -m "lmao, this is funny" -ht "funny" -del 3` The bot will start to search for users in "funny" hashtag and will send a message to each of them. The delay time between each message is 3 seconds.

   - `python Instagram.py -c -del 8 -a` The bot will start to comment on the most recent posts to each of users in user.json file , the comments are taken randomly each time from the comments.json file. The delay time will be 8 seconds, and also when you run the command, the bot will ask you for the account you want to use because of the "-a" param.


3. Follow the prompts in the terminal to provide necessary information, such as login credentials, comments, hashtags, etc.

4. Sit back and let the bot automate the desired actions on Instagram!

### Notes:
- if you provide a hashtag using (-ht) the bot will do the desired action on the user and posts from the hastag. otherwise the bot will take the users provided in users.json file
- if you don't provide a comment using (-cm) the bot will randomly choose comment from comments.json
- if you don't provide a message using (-m) when dming users the bot will randomly choose message from dms.json
- Be cautious when performing automated actions to avoid any potential account restrictions or bans.
