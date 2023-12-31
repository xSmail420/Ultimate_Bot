import argparse
import json
from youtube.YoutubeBot import YoutubeBot

def load_accounts():
        try:
            with open("youtube/accounts.json", "r") as file:
                accounts = json.load(file)
        except FileNotFoundError:
            accounts = []
        return accounts

def load_comments():
        try:
            with open("comments.json", "r") as file:
                comments = json.load(file)
            return comments
        except FileNotFoundError:
            return None
            
def save_accounts(accounts):
    with open("youtube/accounts.json", "w") as file:
        json.dump(accounts, file)

def create_bot(account):
    bot = YoutubeBot()
    bot.youtube_login(email=account["username"], password=account["password"])
    return bot

def main():
    parser = argparse.ArgumentParser(description="Youttube Bot")

    parser.add_argument("-s", "--search", help="search niche to scrape videos from")
    parser.add_argument("-v", "--views", type=int, default=1000, help="Number of max views")
    parser.add_argument("-m", "--market", type=str , default="francais", help="Desired market")
    parser.add_argument("-del", "--delay", type=int, default=5, help="Delay in seconds between actions")
    parser.add_argument("-nb", "--nbVids", type=int, default=5, help="Number of videos to scrape")
    

    args = parser.parse_args()

    # if args.accounts:
    #     accounts = load_accounts()

    #     if len(accounts) == 0:
    #         print("No accounts found. Please add accounts first.")
    #         return

    #     for i, account in enumerate(accounts):
    #         print(f"Account {i+1}: {account['username']}")

    #     account_choice = input("Select an account number: ")

    #     try:
    #         account_choice = int(account_choice)
    #         if account_choice < 1 or account_choice > len(accounts):
    #             print("Invalid account number.")
    #             return
    #     except ValueError:
    #         print("Invalid input.")
    #         return

    #     account = accounts[account_choice - 1]
    #     bot = create_bot(account)
    # else:
    #     username = input("Enter your email: ")
    #     password = input("Enter your password: ")

    #     account = {
    #         "username": username,
    #         "password": password
    #     }
    #     bot = create_bot(account)

    #     save_accounts([account])

    accounts = load_accounts()

    if len(accounts) == 0:
        print("No accounts found. Please add accounts first.")
        return

    for i, account in enumerate(accounts):
        print(f"Account {i+1}: {account['username']}")
        bot = create_bot(account)

        if not args.search:
            print("Please choose (-s) search term to scrape and comment on videos from.")
            break

        comments = load_comments()
        urls = bot.scrape_url_by_keyword(keyword=args.search, market=args.market, viewsMax=args.views, nb=args.nbVids)
        bot.comment_page(urls,comments)
    

    bot.quit()

if __name__ == "__main__":
    main()
    # email = 'dsi31kelibia@gmail.com'
	# password = 'dsi31kelibia123'