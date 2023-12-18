import argparse
import json
from tiktok.TiktokBot import TiktokBot

def load_accounts():
    try:
        with open("tiktok/accounts.json", "r") as file:
            accounts = json.load(file)
    except FileNotFoundError:
        accounts = []
    return accounts

def load_users():
    try:
        with open("tiktok/users.json", "r") as file:
            users = json.load(file)
        return users
    except FileNotFoundError:
        return None
        
def save_accounts(accounts):
    with open("tiktok/accounts.json", "w") as file:
        json.dump(load_accounts() + accounts, file)

def load_dms():
    try:
        with open("dms.json", "r") as file:
            dms = json.load(file)
        return dms
    except FileNotFoundError:
        return None

def load_comments():
    try:
        with open("comments.json", "r") as file:
            comments = json.load(file)
        return comments
    except FileNotFoundError:
        return None
 
def create_bot(account):
    bot = TiktokBot()
    bot.login(username=account["username"], sessionid=account["sessionid"])
    return bot

def main():
    parser = argparse.ArgumentParser(description="Tiktok Bot")

    parser.add_argument("-c", "--comment", action="store_true", help="Comment on posts")
    parser.add_argument("-d", "--dm", action="store_true", help="Send direct messages")
    parser.add_argument("-llp", "--likelatestpost", action="store_true", help="like users latest post")

    # parser.add_argument("-ht", "--hashtag", help="Hashtag to scrape posts from")
    parser.add_argument("-cm", "--commentmessage", help="comment message to post")
    parser.add_argument("-dm", "--message", help="send direct message to users")
    
    parser.add_argument("-nb", "--number", type=int, default=10, help="number of posts to scrape from hashtag")
    parser.add_argument("-del", "--delay", type=int, default=5, help="Delay in seconds between actions")

    args = parser.parse_args()

    accounts = load_accounts()
    usernames = load_users()
    messages = []
    latest_posts = []
    comment_msg = []

    if args.comment:
        if args.commentmessage :
            comment_msg.append(args.commentmessage)
        else :
            comment_msg = load_comments()
    if args.dm:
        if args.message:
            messages.append(args.message)
        else :
            messages = load_dms()

    for i, account in enumerate(accounts):
        print(f"Account {i+1}: {account['username']}")
        bot = create_bot(account)

        for username in usernames:
            latest_posts = ""
            if args.likelatestpost or args.comment:
                latest_posts = bot.User_latest_post(username=username, delay_time=args.delay)
            
            if args.likelatestpost:
                bot.like_posts(link=latest_posts, delay_time=args.delay)

            if args.comment:
                bot.comment_on_posts(link=latest_posts, comment=comment_msg, delay_time=args.delay)
            
            if args.dm:
                print("dming user : " + username)
                bot.send_dm(username=username, message=messages, delay_time=args.delay)

        bot.quit()

if __name__ == "__main__":
    main()
