# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Import Libraries
import requests, os
import pandas as pd
import nltk
import string
import re
import matplotlib.pyplot as plt
import itertools
from collections import Counter
from bs4 import BeautifulSoup
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from nltk.tokenize import word_tokenize
nltk.download(['stopwords','punkt'])

# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []
class ClientSummaryLookup(Action):

    def name(self) -> Text:
        return "action_client_summary"


    def get_text(link_url):
        data = {}
        data_list = []
        print('Scraping: '+link_url)
        try:
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
            page = requests.get(link_url, headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            for para in soup.find_all("p"):
                data_list.append(para.get_text())
            # Clean List-Remove Nulls
            data_list = list(filter(None,data_list))
            # Combine all list items into one string
            data_list_string = " ".join(data_list)
            return data_list_string
        except:
            print("Error with: ",link_url)
            
    def clean_url(url,root_url):
        validate = URLValidator()
        try:
            # Validate If URL Is Actually A URL
            validate(url)
            # Return Only URLs That Start With Rool URL
            if url.startswith(root_url):
                return url
            else:
                return "None"
        except ValidationError as exception:
            return "None"

    def scrape_site(url):
        # Define root URL
        root_url=url.split('/')[0]+'//'+url.split('/')[2]
        # Make Get Request For Root URL
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        # Navigate Through Page Response For All Links
        links = []
        for link in soup.find_all("a"):
            # Append Clean Link By Running Clean_URL Function
            links.append(clean_url(link.get('href'),root_url))
        # Remove None URLs From Link List
        while "None" in links: links.remove("None")
        return links

    def start_scrape(url):
        links=scrape_site(url)
        data={}
        for link_url in links:
            # Append the Data returned in a DICT to a List
            data[link_url]=get_text(link_url)
        # Return the list
        return data

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        url = "www.convergeone.com/about"
        data=start_scrape(url)
        df = pd.DataFrame.from_dict(data, orient='index') 
        df.reset_index(inplace=True)
        df.columns =['url','data']
        df.drop_duplicates(subset = ['url'], inplace=True)
        neededitems = ['/about'] 
        removeditems = ['/topic/','/author/','/all' ,'/page/', '#comments-listing']
        mask = df.url.apply(lambda x: any(item for item in neededitems if item in x))
        df_blog = df[mask]
        mask2 = df_blog.url.apply(lambda x: any(item for item in removeditems if item in x))
        df_blog = df_blog[~mask2]
        df_blog.reset_index(drop=True, inplace=True)
        df_blog.drop([0,1], inplace=True)
        df_blog.reset_index(drop=True)
        dispatcher.utter_message(text=df_blog.iloc[0].data)

        return []
