import streamlit as st
import requests
import re
import pandas as pd
import numpy as np
from datetime import datetime,timedelta
from bs4 import BeautifulSoup
from transformers import pipeline

st.title("Rayo : Your News Companion")
st.write("Hello there! My name is Rayo and I will provide you the latest headline news real time from BBC as well as a summary of the news content. Stay Tuned")

#Select a news category
default_url = "https://www.bbc.com"

category = st.selectbox("Select a news category",("World","Business","Politics","Health","Science","Technology","Entertainment","Sports"))
if category == "World":
    url = "https://www.bbc.com/news/world"
elif category == "Business":
    url = "https://www.bbc.com/news/business"
elif category == "Politics":
    url = "https://www.bbc.com/news/politics"
elif category == "Health":
    url = "https://www.bbc.com/news/health"
elif category == "Science":
    url = "https://www.bbc.com/news/science_and_environment"
elif category == "Technology":
    url = "https://www.bbc.com/news/technology"
elif category == "Entertainment":
    url = "https://www.bbc.com/news/entertainment_and_arts"
elif category == "Sports":
    url = "https://www.bbc.com/sport"

st.write("Here are the latest", category,"news headlines from BBC today")

one_day_ago = datetime.now() - timedelta(days=1)
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the news articles on the page
    articles = soup.find_all('a',class_='qa-heading-link lx-stream-post__header-link')

    # Initialize lists to store article headlines and links
    news_headlines = []
    news_links = []

    # Loop through the articles and extract relevant information
    for article in articles:
        link = article.find('href')
        " ".join(article.text.split())
        news_headlines.append(article.text)

        #Extract link
        string_soup = str(article).replace('<html><body>', '').replace('</body></html>', '').replace('<p>', '').replace('</p>', '')
        pattern = r'href="([^"]*)"'
        match = re.search(pattern, string_soup)
        if match:
            extracted_url = match.group(1)
            news_links.append(default_url + extracted_url)
        else:
            print("No match found.")
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)

news_index = np.arange(1,len(news_headlines)+1)
daily_news_data = pd.DataFrame({'Headline News': news_headlines, 'Link': news_links}, index=news_index)
st.table(daily_news_data['Headline News'])

#Extract Content of the news article
input_index = st.number_input("Enter the index of the news article you want to read", step = 1, min_value = 1, max_value = len(news_headlines))
story_link = daily_news_data.iloc[input_index-1]['Link']

def full_text(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        text = ""
        for paragraph in soup.find_all('p'):
            text += paragraph.get_text() + " "
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)
    return text

st.write("Here is the summary of the news article you selected")
full_story = full_text(story_link)
st.write(full_story)
st.write(story_link)
