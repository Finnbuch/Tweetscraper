
####  Created by Finn Buchrieser ####
###        Twitter Scraper       ####

from math import nan
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import numpy as np
import random

class Twitter_Scraper :

    def __init__(self, config_dict): 
        self.tweet_list = []
        self.driver = ""
        self.whole_df = None
        self.neutral_df = None
        self.positive_df = None
        self.negative_df = None
        self.min_date = pd.Timestamp("2030-05-18 12:00:00", tz="Europe/Brussels")
        self.config_dict = config_dict
        self.search_term = self.config_dict["search_term"]
        self.min_reply = self.config_dict["search_min_replys"]
        self.min_faves = self.config_dict["search_min_faves"]
        self.min_retweets = self.config_dict["search_min_retweets"]
        self.search_language = self.config_dict["language"]
        self.search_until = self.config_dict["search_until"]
        self.search_since = self.config_dict["search_since"]
        self.tweet_ids = set()
        self.account_name = self.config_dict["account_name"]
        self.account_email = self.config_dict["account_email"]
        self.account_password = self.config_dict["account_password"]
    #get tweets function
    def tweet_scraper(self, card):
        try:
            username = card.find_element_by_xpath('.//span').text
        except (NoSuchElementException, StaleElementReferenceException):
            return
        try:
            handle = card.find_element_by_xpath('.//span[contains(text(), "@")]').text
        except (NoSuchElementException, StaleElementReferenceException):
            return
        try:
            postdate = card.find_element_by_xpath('.//time').get_attribute('datetime')
        except (NoSuchElementException, StaleElementReferenceException):
            return
        try:
            comment = card.find_element_by_xpath('.//div[2]/.//div[2]/div[1]/div[1]//span').text
        except (NoSuchElementException, StaleElementReferenceException):
            return
        try:
            responding = card.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
        except (NoSuchElementException, StaleElementReferenceException):
            return
        text = comment + responding
        try:
            reply_count = card.find_element_by_xpath('.//div[@data-testid="reply"]').text
        except (NoSuchElementException, StaleElementReferenceException):
            return
        try:
            retweet_count = card.find_element_by_xpath('.//div[@data-testid="retweet"]').text
        except (NoSuchElementException, StaleElementReferenceException):
            return
        try:
            like_count = card.find_element_by_xpath('.//div[@data-testid="like"]').text
        except (NoSuchElementException, StaleElementReferenceException):
            return
        tweet = (username, handle, postdate, text, reply_count, retweet_count, like_count)
        return tweet

    def collect_tweets(self):
        
        flag = 0
        for i in range(self.config_dict["number_of_repetitions"]):
            if len(self.tweet_list) != 0:
                flag = 1
                self.search_until = self.min_date
            #start driver
            chrome_options = webdriver.ChromeOptions()
            #prefs = {"profile.managed_default_content_settings.images": 2}
            #chrome_options.add_experimental_option("prefs", prefs)
            self.driver = webdriver.Chrome(self.config_dict["path_to_driver"], chrome_options=chrome_options)
            self.driver.set_window_position(0, 0)
            self.driver.set_window_size(1400, 900)

            #login
            url = r'https://twitter.com/login'
            self.driver.get(url)
            time.sleep(random.uniform(2, 3))
            try:
                time.sleep(random.uniform(1, 3))
                user = self.driver.find_element_by_name('username')
                user.send_keys(self.account_name)
                user.send_keys(Keys.RETURN)
                # email.send_keys(input("Input your Email here:"))
                time.sleep(random.uniform(1, 3))
                password = self.driver.find_element_by_name("password")
                password.send_keys(self.account_password)
                #password.send_keys(getpass.getpass())
                password.send_keys(Keys.RETURN)
                print("First login attempt successful")
            except(NoSuchElementException, StaleElementReferenceException):
                print("First login attempt failed")
            
            time.sleep(random.uniform(2, 3))
            if self.driver.current_url != "https://twitter.com/home":
                try:
                    email = self.driver.find_element_by_name('session[username_or_email]')
                    email.send_keys(self.account_email)
                    # email.send_keys(input("Input your Email here:"))
                    password = self.driver.find_element_by_name("session[password]")
                    password.send_keys(self.account_password)
                    #password.send_keys(getpass.getpass())
                    password.send_keys(Keys.RETURN)
                    print("Second login attempt successful")
                except (NoSuchElementException, StaleElementReferenceException):
                    print("Second login attempt failed")

                time.sleep(random.uniform(2, 3))
                if self.driver.current_url != "https://twitter.com/home":
                    try:
                        time.sleep(random.uniform(1, 3))
                        email = self.driver.find_element_by_name('session[username_or_email]')
                        email.send_keys("Tscraper2")
                        # email.send_keys(input("Input your Email here:"))
                        password = self.driver.find_element_by_name("session[password]")
                        password.send_keys("Abcd1234")
                        #password.send_keys(getpass.getpass())
                        password.send_keys(Keys.RETURN)
                        print("Third login attempt successful")
                    except (NoSuchElementException, StaleElementReferenceException):
                        print("Third login attempt failed")
            
            #search for keyword
            time.sleep(random.uniform(2, 4))
            self.driver.refresh()
            time.sleep(random.uniform(1, 2))
            #searching
            search_flag = 0
            try:
                search_Hashtag = self.driver.find_element_by_xpath('//input[@data-testid="SearchBox_Search_Input"]')
                print("Search query successfully found")
                search_flag = 1
            except (NoSuchElementException, StaleElementReferenceException):
                print("Search Query not found, trying again")
            
            if search_flag == 0:
                try:
                    search_Hashtag = self.driver.find_element_by_xpath('//input[@aria-label="Search query"]')
                    print("Search query successfully found")
                except (NoSuchElementException, StaleElementReferenceException):
                    print("Search Query not found")
                
            search_string = self.search_term + self.min_reply + self.min_faves + self.min_retweets + self.search_language
            if flag == 1:
                self.search_until = str(self.search_until)
                search_string = search_string + "until:" + (self.search_until[:10] + " ")
                print(search_string)
                # search_string = search_string + (self.search_until[5:6] + "-")
                # search_string = search_string + (self.search_until[8:9] + " ")
            else :
                search_string = search_string + self.search_until
            search_string = search_string + self.search_since
            search_Hashtag.send_keys(search_string)
            search_Hashtag.send_keys(Keys.RETURN)
            time.sleep(random.uniform(1, 3))
            latest_Tab = self.driver.find_element_by_xpath("//div[contains(text(),'Latest')]")
            latest_Tab.click()

            #extract information
            
            last_position = self.driver.execute_script("return window.pageYOffset;")
            scrolling = True

            #loop to add certain amount of tweets 
            while scrolling:
                time.sleep(0.5)
                cards = self.driver.find_elements_by_xpath('//article[@data-testid="tweet"]')

                for card in cards[-15:]:
                    tweet = self.tweet_scraper(card)
                    if pd.to_datetime(tweet[2]) < pd.to_datetime(self.min_date):
                        self.min_date = tweet[2]
                    if tweet:
                        tweet_id = ''.join(tweet)
                        if tweet_id not in self.tweet_ids:
                            self.tweet_ids.add(tweet_id)
                            self.tweet_list.append(tweet)
                if len(self.tweet_list) >= self.config_dict["number_of_tweets"] * (i + 1):
                    break
                
                scroll_attempt = 0
                while True:
                    print(len(self.tweet_list))
                    self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    time.sleep(0.75)
                    curr_position = self.driver.execute_script("return window.pageYOffset;")
                    if last_position == curr_position:
                        scroll_attempt += 1

                        if scroll_attempt >= 5:
                            scrolling = False
                            break
                        else : 
                            time.sleep(0.75)
                    else:
                        last_position = curr_position
                        break
            self.driver.quit()

    def preprocessing_data(self):
        #Safe to a Pandas Dataframe
        df = pd.DataFrame(self.tweet_list, columns =['name', 'handle', 'date', 'text', 'replys', 'retweets', 'likes'])
        #self.driver.quit()
        df.replace('', np.nan, inplace =True)
        df.replace(nan, np.nan, inplace=True)
        df.dropna()
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values(by="date")
        df.to_csv(self.config_dict["results_path"], sep = ",", index=False)
        #Analyze Sentiment of Text
        analyser = SentimentIntensityAnalyzer()
        def sentiment_scores(sentence):
            snt = analyser.polarity_scores(sentence)
            return snt
        sentiment_list = []
        for value in df.text:
            sentiment_list.append(sentiment_scores(value)["compound"])
        df["compound"] = sentiment_list

        #calculating rolling mean of compound sentiment
        df['sentiment'] = sentiment_list
        df["rolling_sentiment"] = df["sentiment"].rolling(7).mean()
        self.whole_df = df
        self.positive_df = df[df["compound"] > 0.3]
        self.neutral_df = df[(df["compound"] >= -0.3) & (df["compound"] <= 0.3)]
        self.negative_df = df[df["compound"] < -0.3]