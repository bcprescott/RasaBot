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
            
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:



        dispatcher.utter_message(text="Hello World!")

        return []
