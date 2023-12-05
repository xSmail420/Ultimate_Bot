import time
import json
import random
from datetime import datetime as dt
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class TiktokBot:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--window-size=930,820")
        chrome_options.add_argument("--start-maximized")  # Maximize the Chrome window
        # Use webdriver_manager to automatically download and manage the ChromeDriver
        # add undetected_chromedriver here 
        self.driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element(By.XPATH,xpath)
        except NoSuchElementException:
            return False
        return True
    
    def login(self,username, sessionid ):
        self.driver.get("https://www.tiktok.com")
        time.sleep(3)
        self.driver.add_cookie({'name': 'sessionid', 'value': f'{sessionid}'})
        self.driver.get("https://www.tiktok.com")
        time.sleep(5)
        if (self.check_exists_by_xpath('//*[@id="app-header"]/div/div[3]/div[3]')):
            print(f'Logged in as : {username} ')
        else:
            print("user sessionid incorrect or expired !")
            self.quit()

    def scrape_hashtag_posts(self, tag,DesiredVidsNumber):
        print("getting tiktoks from hashtag...")
        videos = []
        try:
            self.driver.get(f"https://www.tiktok.com/search/video?q=%23{tag}")
            time.sleep(5)

            while True :
                try :
                    self.driver.find_element(By.ID,'verify-bar-close').click()
                    self.driver.refresh()
                except : 
                    pass
                self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(3)
                vlist=self.driver.find_elements(By.CLASS_NAME ,'e19c29qe10')
                
                for elem in vlist :
                    if len(videos) == DesiredVidsNumber :
                        print(f'{len(videos)} Videos selected for : {tag} ')
                        return videos
                    link=elem.find_element(By.CLASS_NAME,'e1cg0wnj1').find_element(By.TAG_NAME ,'a').get_attribute('href')
                    print(link)
                    videos.append(link)
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def scrape_usernames(self, links):
        print("getting usernames...")
        usernames = []
        for url in links:
            try:
                # Find the starting and ending indices for the username
                start_index = url.find('@') + 1
                end_index = url.find('/video/')

                # Extract the username using slicing
                if start_index != -1 and end_index != -1:
                    username = url[start_index:end_index]
                    usernames.append(username)
            except Exception as e:
                print(f"An error occurred: {e}")
        # Remove duplicate usernames
        usernames = list(set(usernames))
        
        return usernames
    
    def send_dm(self, usernames, message, delay_time):
            print("sending users dierect messages...")
            for username in usernames:
                try :
                    # Go to the Instagram Direct Inbox
                    self.driver.get(f"https://www.tiktok.com/@{username}")
                    time.sleep(3)
                    msg =  random.choice(message)
                    # Click the 'New Message' button
                    new_message_button = self.driver.find_element(By.XPATH, '//*[@id="main-content-others_homepage"]/div/div[1]/div[1]/div[2]/div/div[2]/a').get_attribute("href")
                    self.driver.get(new_message_button)
                    time.sleep(4)
                    
                    wait = WebDriverWait(self.driver, 10)
                    wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Send a message...")]')))

                    msg_input = self.driver.find_element(By.XPATH, '//div[contains(text(), "Send a message...")]')
                    msg_input.click()
                    time.sleep(1)
                    # Create an instance of ActionChains
                    actions = ActionChains(self.driver,duration=1000)
                    actions.send_keys(msg)
                    actions.send_keys(Keys.RETURN)
                    # Perform the actions
                    actions.perform()

                    time.sleep(delay_time)
                except Exception as e:
                    print(f"An error occurred: {e}")
    
    def comment_on_posts(self, links, comment, delay_time):
        print("commenting on users post...")
        for link in links:
            try:
                cm =  random.choice(comment)
                # Open each post link
                self.driver.get(link)
                time.sleep(2)   
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.presence_of_element_located((By.XPATH,'//div[contains(text(), "Add comment...")]')))

                # Find the comment input field
                comment_input = self.driver.find_element(By.XPATH, '//div[contains(text(), "Add comment...")]')
                comment_input.click()
                time.sleep(1)

                # Create an instance of ActionChains
                actions = ActionChains(self.driver,duration=1000)
                actions.send_keys(cm)
                actions.send_keys(Keys.RETURN)
                # Perform the actions
                actions.perform()

                time.sleep(delay_time)
            except Exception as e:
                print(f"An error occurred: {e}")

    def like_posts(self, links, delay_time):
        print("liking posts...")
        for link in links :
            try:
                # Open posts
                self.driver.get(link)
                time.sleep(5)
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.presence_of_element_located((By.XPATH,'//div[contains(@class,"DivActionItemContainer")]/button[1]')))
                
                # Locate and click on the like button
                like_button = self.driver.find_element(By.XPATH, '//div[contains(@class,"DivActionItemContainer")]/button[1]')
                
                like_button.click()
                time.sleep(delay_time)
            except Exception as e:
                print(f"An error occurred: {e}")
    
    def User_latest_post(self, usernames, delay_time):
        users_liked_post_links = [] # //div[1]/div/div/a/div[2]/div/div
        print("getting users post...")
        for username in usernames : 
            try:
                # Open tiktok and navigate to the user stories page
                self.driver.get(f"https://www.tiktok.com/@{username}/")
                time.sleep(5)
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-content-others_homepage"]/div/div[2]')))
                #                                                //*[@id="main-content-others_homepage"]/div/div[2]/div[2]/div
                most_recent = self.driver.find_elements(By.CLASS_NAME, 'css-x6y88p-DivItemContainerV2')
                nb_pinned = len(self.driver.find_elements(By.XPATH, '//div[1]/div/div/a/div[2]/div/div'))
                # Scrape the most recent posts from the profile
                # print(username)
                # print(len(most_recent))
                # print(nb_pinned)
                # Retrieve the href attribute value
                href = most_recent[nb_pinned].find_element(By.TAG_NAME, "a").get_attribute("href")
                print(href)
                users_liked_post_links.append(href)
                time.sleep(delay_time)
            except Exception as e:
                print(f"An error occurred: {e}")
        return users_liked_post_links

    def quit(self):
        print("Exist.")
        self.driver.quit()