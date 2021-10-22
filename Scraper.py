
from Twitter_Plotter import LinePlotter, WordCloudGeneration
from Python_twitter_scraper import Twitter_Scraper
from config_reader import ConfigReader

Config_reader = ConfigReader()
config_dict = ConfigReader.read_json_config("C:\\Users\\finnb\\OneDrive\\Dokumente\\Neuropsycho\\Twitter_scraper\\Tweetscraper\\config.json")
#config_dict = ConfigReader.read_json_config("C:\\Users\\buchries\\Documents\\Twitter_scraping\\Tweetscraper\\config.json")
#Getting the tweets
scraper = Twitter_Scraper(config_dict)
scraper.collect_tweets()
scraper.preprocessing_data()

dataframe = scraper.whole_df

positive_dataframe = scraper.positive_df
negative_dataframe = scraper.negative_df
neutral_dataframe = scraper.neutral_df

whole_text = []
positive_text = []
negative_text = []
neutral_text = []
dataframe_list = [dataframe, neutral_dataframe, negative_dataframe, positive_dataframe]
text_list = [whole_text, neutral_text, negative_text, positive_text]

for counter, dataset in enumerate(dataframe_list):
    for text in dataset.text:
        text_list[counter].append(text)

#plotting the sentiment over time
lineplot = LinePlotter()
lineplot.mood_over_time(dataframe["date"], dataframe["rolling_sentiment"])

#filtering data and creating a wordcloud
title_list = ["All Words", "Neutral Words", "Negative Words", "Positive Words"]
wordcloud_generator = WordCloudGeneration()
clean_text_list = []
for text in text_list:
    clean_data = wordcloud_generator.preprocessing(text)
    clean_text_list.append(clean_data)
wordcloud_generator.create_word_cloud(clean_text_list, title_list)
