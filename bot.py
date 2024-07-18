import time
from selenium.webdriver.support import expected_conditions as EC
from config import CONFIG
from credentials import CREDENTIALS
from twitter import TwitterBot
from utils import waitForPage

def main_menu(Twitter_bot):
    while True:
        print("1. Tweet")
        print("2. Follow")
        print("3. Unfollow")
        print("4. Search")
        print("5. Quit")
        print("6. Home")

        choice = input("Enter your choice: ")

        if choice == "1":
            context = input("Enter the tweet: ")
            Twitter_bot.tweet(context)
        elif choice == "2":
            user = input("Enter the username of the user to follow: ")
            Twitter_bot.follow(user)
        elif choice == "3":
            user = input("Enter the username of the user to unfollow: ")
            Twitter_bot.unfollow(user)
        elif choice == "4":
            query = input("Enter the search query: ")
            Twitter_bot.search(query)
        elif choice == "5":
            return
        elif choice == "6":
            Twitter_bot.home()
        else:
            print("Invalid choice")

def main():
    Twitter_bot = TwitterBot(CREDENTIALS['username'], CREDENTIALS['password'])
    Twitter_bot.login()
    
    while True:
        main_menu(Twitter_bot)
        print(f"SLEEPING FOR {CONFIG['check_interval']} SECONDS...")
        time.sleep(CONFIG['check_interval'])

if __name__ == "__main__":
    main()

