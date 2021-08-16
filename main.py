from selenium import webdriver
from time import sleep
import os


CHROME_DRIVER_PATH = "C:\Program Files\Development\chromedriver.exe"
INTERNET_PROVIDER = "Beeline" #your Internet provider
PROMISED_DOWN = 100 #or whichever download speed your provider guarantees you
PROMISED_UP = 5 #or whichever upload speed your provider guarantees you
TWITTER_USERNAME = os.environ.get("TWITTER_USERNAME")
TWITTER_PASSWORD = os.environ.get("TWITTER_PASSWORD")


class InternetSpeedTwitterBot:
    def __init__(self, driver_path):
        self.driver = webdriver.Chrome(driver_path)
        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")

        sleep(15)

        measure_button = self.driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a/span[4]')
        measure_button.click()
        sleep(60)
        self.down = int(self.driver.find_element_by_class_name("download-speed").text)
        sleep(20)
        self.up = int(self.driver.find_element_by_class_name("upload-speed").text)

        self.driver.quit()

    def tweet_at_provider(self):
        self.driver.get("https://twitter.com")

        sleep(3)

        login_button = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div[3]/a[2]/div/span/span')
        login_button.click()

        username_field = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label/div/div[2]/div/input')
        username_field.send_keys(TWITTER_USERNAME)
        #
        password_field = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]/div/input')
        password_field.send_keys(TWITTER_PASSWORD)
        #
        sleep(5)
        login_field = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div/div/span/span')
        login_field.click()
        #
        tweet = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div/div/div/div')
        tweet.send_keys(f"Hey @{INTERNET_PROVIDER}! Why is my internet speed just {self.down}/{self.up} when I'm paying for {PROMISED_DOWN}/{PROMISED_UP}?")

        sleep(5)

        tweet_submit = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div/div/span/span')
        tweet_submit.click()

        self.driver.quit()


my_bot = InternetSpeedTwitterBot(CHROME_DRIVER_PATH)
my_bot.get_internet_speed()

if my_bot.up < PROMISED_UP or my_bot.down < PROMISED_DOWN:
    my_bot.tweet_at_provider()



