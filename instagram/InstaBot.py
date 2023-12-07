import time
import json
import random
from datetime import datetime as dt
#from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class InstagramBot:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--window-size=930,820")
        # chrome_options.add_argument("--start-maximized")  # Maximize the Chrome window
        # Use webdriver_manager to automatically download and manage the ChromeDriver
        # add undetected_chromedriver here 
        self.driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def login(self, email, password):
        # Open Instagram
        self.driver.get("https://www.instagram.com/")
        # Wait for the login elements to become available
        wait = WebDriverWait(self.driver, 10)
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        
        password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        
        # Find the login elements and enter email and password
        email_field.send_keys(email)
        time.sleep(3)
        password_field.send_keys(password)
        time.sleep(1)
        # Submit the login form
        password_field.send_keys(Keys.RETURN)

        # Wait for the login process to complete (you may need to adjust the delay based on your internet speed)
        time.sleep(10)  # Wait for 5 seconds (adjust as needed)

    def scrape_hashtag_posts(self, hashtag):
        links = []
        try:
            # Open Instagram and navigate to the hashtag page
            self.driver.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
            time.sleep(8)
            # Wait for the posts to load
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.XPATH, '//div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/article/div/div/div')))

            most_recent = self.driver.find_element(By.XPATH, '//div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/article/div/div/div')
            
            # Scrape the most recent posts from the hashtag
            posts = most_recent.find_elements(By.TAG_NAME, "a")

            
            for post in posts:
                # Retrieve the href attribute value
                href = post.get_attribute("href")
                # Process each href as needed
                links.append(href)
        except:
            pass    
        
        return links
    
    def scrape_usernames(self, links):
        usernames = []
        for link in links:
            try:
                self.driver.get(link)
                time.sleep(3)
                # Wait for the username element to load
                wait = WebDriverWait(self.driver, 10)
                usernames_element = wait.until(EC.presence_of_element_located((By.XPATH, '//div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/div[1]/div[1]')))
                #                                                                        //div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/div[1]/div[1] -- /div/span/span/div/a -- /span/div[1...]/div/a
                # Find elements with the specified tag name
                users = usernames_element.find_elements(By.TAG_NAME, "a")

                # Ensure users is always a list
                if not isinstance(users, list):
                    users = [users]

                # Process each user
                for username in users:
                    # Extract the username text
                    name = username.text
                    usernames.append(name)
            
            except:
                pass
        # Remove duplicate usernames
        usernames = list(set(usernames))
        
        return usernames
    
    def send_dm(self, usernames, message, delay_time):
        
        try:
            # Go to the Instagram Direct Inbox
            self.driver.get("https://www.instagram.com/direct/inbox/")
            time.sleep(8)

            try:
                notification_popup = self.driver.find_element(By.XPATH, '//div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]')
                
                if notification_popup.is_displayed():
                    notification_popup.click()
                    time.sleep(2)
            except:
                pass
                
            try :
                msg =  random.choice(message)
                # Click the 'New Message' button        
                new_message_button = self.driver.find_element(By.XPATH, '//div/*[@aria-label="New message"]')
                new_message_button.click()
                time.sleep(2)
                # Wait for the recipient input field to become available
                wait = WebDriverWait(self.driver, 10)
                recipient_input = wait.until(EC.presence_of_element_located((By.XPATH, '//div/div[2]/div/div/div/div/div/div/div[1]/div/div[2]/div/div[2]/input')))

                # Type each username and press Enter to add as a recipient
                recipient_input.send_keys(usernames)
                time.sleep(1)
                recipient_input.send_keys(Keys.ENTER)            
                time.sleep(1)

                    
                select_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div')))
                select_button.click()
                time.sleep(2)

                # Wait for the next button to become clickable
                next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[4]/div')))

                # Click the Next button to proceed to the message input
                next_button.click()
                time.sleep(3)

                # Create an instance of ActionChains
                actions = ActionChains(self.driver,duration=1000)
                actions.send_keys(msg)
                actions.send_keys(Keys.RETURN)
                # Perform the actions
                actions.perform()

                time.sleep(delay_time)
            except Exception as e:
	            print("ERROR fel send dm : "+str(e))
        except:
            pass

    def comment_on_posts(self, links, comment, delay_time):
        
            try:
                cm =  random.choice(comment)
                # Open each post link
                self.driver.get(links)
                time.sleep(2)

                # Find the comment input field
                comment_input = self.driver.find_element(By.CSS_SELECTOR, 'textarea[aria-label="Add a comment…"]')
                comment_input.click()
                time.sleep(1)

                # Create an instance of ActionChains
                actions = ActionChains(self.driver,duration=1000)
                actions.send_keys(cm)
                actions.send_keys(Keys.RETURN)
                # Perform the actions
                actions.perform()

                time.sleep(delay_time)
            except:
                pass

    def like_stories(self, usernames, delay_time):
        
            try:
                
                # Open Instagram and navigate to the user stories page
                self.driver.get(f"https://www.instagram.com/stories/{usernames}/")
                time.sleep(8)
   
                # Wait for the stories to load
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.presence_of_element_located((By.XPATH, '//div/div/div/div[1]/div[1]/section/div[1]/div/div/div/div[2]/div/div[3]/div')))

                # Check if the view stories pop-up is displayed
                view_stories_popup = self.driver.find_element(By.XPATH, '//div/div/div/div[1]/div[1]/section/div[1]/div/div/div/div[2]/div/div[3]/div')
                
                if view_stories_popup.is_displayed():
                    view_stories_popup.click()
                    time.sleep(2)

                stories = self.driver.find_element(By.XPATH, '//section/div[1]/div/div/div[1]/div[1]/div[1]')
                # Get all child elements of the element
                children = stories.find_elements(By.XPATH, '*')
                # Get the number of stories
                for _ in children :
                    # Locate and click on the like button
                    like_button = self.driver.find_element(By.XPATH, '//span[@class="x1i64zmx"]/div')
                    like_button.click()
                    time.sleep(1)
                    # Locate and click on the next button
                    like_button = self.driver.find_element(By.XPATH, '//div/div/div/div[1]/div[1]/section/div[1]/div/div/div[2]/div[2]/div')
                    like_button.click()
                    time.sleep(1)


                time.sleep(delay_time)
            except:
                #print(f"Error occured while trying to access User \"{username}\" stories")
                pass

    def like_posts(self, links, delay_time):
        
            try:
                # Open posts
                self.driver.get(links)
                # Locate and click on the like button
                like_button = self.driver.find_element(By.XPATH, '//div/div[3]/div[1]/div[1]/span[1]/div')
                like_button.click()
                time.sleep(delay_time)
            except:
                #print(f"Error occured while trying to access User \"{username}\" stories")
                pass

    def User_latest_post(self, usernames, delay_time): 
        latest_post = ""
        try:
                # Open Instagram and navigate to the user stories page
                self.driver.get(f"https://www.instagram.com/{usernames}/")

                # Wait for the stories to load
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.presence_of_element_located((By.XPATH, '//div/div[3]/article/div[1]/div')))

                most_recent = self.driver.find_element(By.XPATH, '//div/div[3]/article/div[1]/div')
            
                # Scrape the most recent posts from the profile
                posts = most_recent.find_elements(By.TAG_NAME, "a")
                links = []
                for post in posts[:4]:
                    # Retrieve the href attribute value
                    href = post.get_attribute("href")
                    # Process each href as needed
                    links.append(href)
                time.sleep(delay_time)

                dates = []
                #get the posts date
                for link in links :
                    self.driver.get(link)
                    time.sleep(3)
                    # Wait for the username element to load
                    wait = WebDriverWait(self.driver, 10)
                    wait.until(EC.presence_of_element_located((By.XPATH, '//div/div[2]/div/div[3]/div[2]/div/a/span/time')))
                    time_element = self.driver.find_element(By.XPATH, '//div/div[2]/div/div[3]/div[2]/div/a/span/time' )
                    time_string = time_element.get_attribute('datetime')
                    dates.append(dt.fromisoformat(time_string.split('.')[0]))
                # Identify the latest post
                latest_post = links[dates.index(max(dates))]
                
        except:
                pass
        return latest_post

    def quit(self):
        self.driver.quit()