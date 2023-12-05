import argparse
import json
from instagram.InstaBot import InstagramBot


def load_accounts():
        try:
            with open("instagram/accounts.json", "r") as file:
                accounts = json.load(file)
        except FileNotFoundError:
            accounts = []
        return accounts

def load_users():
        try:
            with open("instagram/users.json", "r") as file:
                users = json.load(file)
            return users
        except FileNotFoundError:
            return None

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
        
def save_accounts(accounts):
    with open("instagram/accounts.json", "w") as file:
        json.dump(load_accounts() + accounts, file)

def create_bot(account):
    bot = InstagramBot()
    bot.login(email=account["username"], password=account["password"])
    return bot

def main():
    parser = argparse.ArgumentParser(description="Instagram Bot")

    parser.add_argument("-a", "--accounts", action="store_true", help="Use multiple accounts")
    parser.add_argument("-c", "--comment", action="store_true", help="Comment on posts")
    parser.add_argument("-d", "--dm", action="store_true", help="Send direct messages")
    parser.add_argument("-ls", "--likestories", action="store_true", help="like all current users stories")
    parser.add_argument("-llp", "--likelatestpost", action="store_true", help="like users latest post")

    parser.add_argument("-ht", "--hashtag", help="Hashtag to scrape posts from")
    parser.add_argument("-cm", "--commentmessage", help="comment message to post")
    parser.add_argument("-dm", "--message", help="send direct message to users")

    parser.add_argument("-del", "--delay", type=int, default=5, help="Delay in seconds between actions")

    args = parser.parse_args()

    if args.accounts:
        accounts = load_accounts()

        if len(accounts) == 0:
            print("No accounts found. Please add accounts first.")
            return

        for i, account in enumerate(accounts):
            print(f"Account {i+1}: {account['username']}")

        account_choice = input("Select an account number: ")

        try:
            account_choice = int(account_choice)
            if account_choice < 1 or account_choice > len(accounts):
                print("Invalid account number.")
                return
        except ValueError:
            print("Invalid input.")
            return

        account = accounts[account_choice - 1]
        bot = create_bot(account)
    else:
        username = input("Enter your Instagram username: ")
        password = input("Enter your Instagram password: ")

        account = {
            "username": username,
            "password": password
        }
        save_accounts([account])
        bot = create_bot(account)

        

    if args.hashtag :
        hashtag = args.hashtag
        latest_posts = bot.scrape_hashtag_posts(hashtag=hashtag)
        usernames = bot.scrape_usernames(links=latest_posts)
    else :
        usernames = load_users()
        latest_posts = bot.User_latest_post(usernames=usernames, delay_time=args.delay)

    if args.dm:
        messages = []
        if args.message:
            messages.append(args.message)
        else :
            messages = load_dms()
        bot.send_dm(usernames=usernames, message=messages, delay_time=args.delay)

    if args.likestories:
        bot.like_stories(usernames=usernames, delay_time=args.delay)
        
    if args.likelatestpost:
        bot.like_posts(links=latest_posts, delay_time=args.delay)

    if args.comment:
        comment_msg = []
        if args.commentmessage :
            comment_msg.append(args.commentmessage)
        else :
            comment_msg = load_comments()
        bot.comment_on_posts(links=latest_posts, comment=comment_msg, delay_time=args.delay)

    bot.quit()

if __name__ == "__main__":
    main()