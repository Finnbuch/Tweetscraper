
from nltk.corpus import stopwords
from nltk.corpus.reader.chasen import test
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
from nltk.corpus.reader.comparative_sents import ComparativeSentencesCorpusReader
import numpy as np
from PIL import Image


class LinePlotter:
    def mood_over_time(self, xaxis, yaxis):
        #plotting sentiment
        plt.figure(figsize=(12,10))
        plt.plot(xaxis, yaxis)
        plt.xticks(rotation = 90)
        plt.title("Valence of Topic over Time")
        plt.show()

class WordCloudGeneration:
    def preprocessing(self, data):
        # convert all words to lowercase
        data = [item.lower() for item in data]
        # load the stop_words of english
        stop_words = set(stopwords.words('english'))
        # concatenate all the data with spaces.
        paragraph = ' '.join(data)
        # tokenize the paragraph using the inbuilt tokenizer
        word_tokens = word_tokenize(paragraph) 
        # filter words present in stopwords list
        full_words = []
        nono_words = ["n't", "'s"]
        for word in word_tokens:
            if len(word) > 2 and word not in nono_words:
                full_words.append(word)
        preprocessed_data = ' '.join([word for word in full_words if not word in stop_words])
        return preprocessed_data

    def create_word_cloud(self, final_data):
        # initiate WordCloud object with parameters width, height, maximum font size and background color
        # call the generate method of WordCloud class to generate an image

        wordcloud = WordCloud(width=1600, height=800, max_font_size=200, background_color="black", max_words= 50).generate(final_data)
        # plt the image generated by WordCloud class
        return wordcloud

    def create_word_cloud(self, clean_text_list, title_list):
            for i, text in enumerate(clean_text_list):
                
                wordcloud = WordCloud(width=1600, height=800, max_font_size=200, background_color="black", max_words= 50).generate(text)
                plt.figure(figsize=(12,10))
                plt.imshow(wordcloud)
                plt.axis('off')
                plt.title(title_list[i])
                plt.show()
