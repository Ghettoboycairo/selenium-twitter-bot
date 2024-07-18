import time
from xml.etree.ElementTree import SubElement
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import click_with_retry, wait_for_element, waitForPage
from credentials import CREDENTIALS
from config import CONFIG, ELEMENTS

class TwitterBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()
        self.loggedIn = False

    def login(self):
        self.driver.get(CONFIG["websiteAddress"])

        wait_for_element(self.driver, ELEMENTS["signInButton"]).click()

        print("Found the 'Sign In' button, clicking...")
        
        usernameField = wait_for_element(self.driver, ELEMENTS["usernameField"])
        usernameField.send_keys(self.username)
        print("Entered username...")

        click_with_retry(self.driver, ELEMENTS["nextButton"])
        print("Clicked next...")

    
        #going to wait for phone or email verification but for only 15 seconds
        phoneNumberField = wait_for_element(self.driver, ELEMENTS["phoneNumberField"],False,3)
        passwordField = wait_for_element(self.driver, ELEMENTS["passwordField"],False,3)
        print("Akherna hena..")

        while self.loggedIn == False:
            phoneNumberField = wait_for_element(self.driver, ELEMENTS["phoneNumberField"],False,3)
            passwordField = wait_for_element(self.driver, ELEMENTS["passwordField"],False,3)
            if (phoneNumberField or passwordField) == None:
                print("didn't get asked for phone verification or password, solve the captcha...")
                time.sleep(5)

            if phoneNumberField is not None:
                phoneNumberField.send_keys(CREDENTIALS["phoneOrEmail"])
                nextButton = wait_for_element(self.driver, ELEMENTS["nextButton2"])
                nextButton.click()
                print("bypassed E-Mail verification, clicked next...")
                phoneNumberField = None

            if passwordField is not None:
                passwordField.send_keys(self.password)
                print("Entered password...")
                click_with_retry(self.driver, ELEMENTS["loginButton"])
                print("Pressed login...")
                self.loggedIn = True

    def home(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ELEMENTS["homeButton"])
            )
        ).click()

    def tweet(self,context):
        if self.loggedIn ==True:
            self.home()
            tweetField = wait_for_element(self.driver,ELEMENTS["tweetField"])
            tweetField.clear()
            tweetField.send_keys(context)
            print("filled the tweet textfield...")

            tweetButton = wait_for_element(self.driver, ELEMENTS["tweetButton"])
            tweetButton.click()
            print("pressed tweet..")
            return
        else:
            print("account is not logged in...")
            return
    
    def search(self,username):
        click_with_retry(self.driver,ELEMENTS["exploreButton"])
        print("clicked the explore button...")
        searchBar = wait_for_element(self.driver,ELEMENTS["searchBar"])
        searchBar.click()
        searchBar.clear()
        print("clicked and cleared the search bar...")
        
        searchBar.send_keys(username)
        print("sent the account username to the search bar...")
        
        # goToUserAccount = wait_for_element(self.driver,ELEMENTS["goToUserAccount"])
        goToUserAccount = WebDriverWait(self.driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, ELEMENTS["goToUserAccount"])))
        goToUserAccount.click()
        print("one")
        goToUserAccount.click()
        print("two")
        goToUserAccount.click()
        print("three")



    def follow(self,username):
        self.search(username)
        followButtonSpan = wait_for_element(self.driver,ELEMENTS["followButtonSpan"])
        
        if followButtonSpan.text == "Follow":
            print("you're not following the account...")
        
            followButton = wait_for_element(self.driver,ELEMENTS["followButton"])
            followButton.click()
        
            if(followButton.text == "Following"):
                print("now following...")
                return
            elif(followButton.text == "Pending"):
                print("pending...")
                return
            else:
                print("failed to follow...")
                return
        else:
            print("already following...")
            return

    def unfollow(self,username):
        self.search(username)
        
        unfollowButtonSpan = wait_for_element(self.driver,ELEMENTS["unfollowButtonSpan"])
        print("found unfollow button...")

        if unfollowButtonSpan.text == "Following":
            print("you're following the account...")

            unfollowButton = wait_for_element(self.driver,ELEMENTS["unfollowButton"])
            unfollowButton.click()
           
            confirmButton = wait_for_element(self.driver, ELEMENTS["confirmButton"])
            confirmButton.click()
            confirmButton.click()
           
            if (unfollowButtonSpan.text == "Follow"):
                print("now not following...")
                return
            else:
                print("failed to unfollow...")
                return
        else:
            print("already not following...")
            return

