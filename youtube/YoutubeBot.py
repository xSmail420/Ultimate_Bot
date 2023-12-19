import time
import random
import numpy as np
import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class YoutubeBot:
	def __init__(self) :
		op = webdriver.ChromeOptions()
		op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
		# op.add_argument('--headless')
		op.add_argument('--disable-dev-shm-usage')
		op.add_argument('--no-sandbox')
		self.driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=op)

	def youtube_login(self, email, password):
		self.driver.get('https://accounts.google.com/ServiceLogin?hl=en&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fhl%3Den%26feature%3Dsign_in_button%26app%3Ddesktop%26action_handle_signin%3Dtrue%26next%3D%252F&uilel=3&passive=true&service=youtube#identifier')
		
		wait = WebDriverWait(self.driver, 30)
		wait.until(EC.presence_of_element_located((By.ID, 'identifierId')))
		
		self.driver.find_element(By.ID, 'identifierId').send_keys(email)
		self.driver.find_element(By.ID, 'identifierNext').click()
		time.sleep(10)
		#WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div#password input[name="password"]')))
		wait.until(EC.presence_of_element_located((By.ID, 'passwordNext')))
		self.driver.find_element(By.XPATH,'//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
		time.sleep(4)
		self.driver.find_element(By.ID, 'passwordNext').click()
		time.sleep(4)

	def comment_page(self, urls, comments):

		if len( urls ) == 0:
			print ('Youtube Comment Bot: Finished!')
			return []
		
		url = urls.pop()
		time.sleep(4)
		self.driver.get(url)
		print(url)
		self.driver.implicitly_wait(1)

		if not self.check_exists_by_xpath('//*[@id="movie_player"]'):
			return self.comment_page(urls, comments)
		time.sleep(4)
		self.driver.execute_script("window.scrollTo(0, 600);")
		
		if not self.check_exists_by_xpath('//*[@id="simple-box"]/ytd-comment-simplebox-renderer'):
			return self.comment_page( urls, comments)

		if self.check_exists_by_xpath('//*[@id="contents"]/ytd-message-renderer'):
			return self.comment_page( urls, comments)

		WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-comments ytd-comment-simplebox-renderer")))
		time.sleep(4)
		self.driver.find_element(By.CSS_SELECTOR , "ytd-comments ytd-comment-simplebox-renderer div#placeholder-area").click()
		self.driver.implicitly_wait(5)

		wait = WebDriverWait(self.driver, 10)
		wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="contenteditable-root"]')))
                
		self.driver.find_element(By.XPATH,'//*[@id="contenteditable-root"]').send_keys(self.random_comment(comments))
		self.driver.find_element(By.XPATH ,'//*[@id="contenteditable-root"]').send_keys(Keys.CONTROL, Keys.ENTER)

		post = WebDriverWait(self.driver, 15).until(
			EC.element_to_be_clickable((By.CSS_SELECTOR,'ytd-comments ytd-comment-simplebox-renderer'))
		)
		post.click()

		r = np.random.randint(2,5)
		time.sleep(r)

		return self.comment_page(urls,comments)

	def random_comment(self, comments):
		return random.choice(comments)
	
	def check_exists_by_xpath(self, xpath):
		try:
			self.driver.find_element(By.XPATH,xpath)
		except NoSuchElementException:
			return False
		return True

	def scrape_url_by_keyword(self, keyword, market, viewsMax, nb):
		links = []
		try:
			self.driver.get(f"https://www.youtube.com/results?search_query={keyword}+{market}&sp=EgQIBBAB") #//ytd-video-renderer
			
			while (len(links) < nb):
				print(f"{len(links)} links/{nb}")
				time.sleep(5)
				# Wait for the username element to load
				wait = WebDriverWait(self.driver, 10)
				wait.until(EC.presence_of_element_located((By.XPATH, '//ytd-video-renderer')))
				videos = self.driver.find_elements(By.XPATH, '//ytd-video-renderer')
				# Find elements with the specified tag name
				for video in videos :
					views = video.find_element(By.XPATH, ".//div[2]/span[1]").text
					if (self.filter_views(views,viewsMax)):
						links.append(video.find_element(By.XPATH, ".//ytd-thumbnail/a").get_attribute("href").replace("/shorts/", "/watch?v="))
						links = list(set(links))
				self.driver.find_element(By.TAG_NAME,'body').send_keys(Keys.END)

		except:
			pass
		
		return links

	def filter_views(self ,objet, views):
		valeur_en_nombre = self.convertir_en_nombre(objet)
		return valeur_en_nombre < views
	
	def convertir_en_nombre(self ,valeur):
		multiplicateurs = {'K': 1000, 'M': 1000000}
		for suffixe, facteur in multiplicateurs.items():
			if suffixe in valeur:
				return float(valeur.replace(f'{suffixe} views', '')) * facteur
		return float(valeur.replace(' views', ''))

	def quit(self):
		self.driver.quit()