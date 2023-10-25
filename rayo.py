import streamlit as st
import requests
import re
import pandas as pd
import numpy as np
from datetime import datetime,timedelta
from bs4 import BeautifulSoup
from transformers import pipeline
from transformers import AutoTokenizer, TFBartForConditionalGeneration


st.title("Stay Informed with Rayo")
st.subheader("The Ultimate News Companion")

st.write('''
In a world overflowing with information, staying informed with the correct news is vital. Rayo is your tursted ally in the pursuit of the most recent and relevant news from BBC. Choose from the category that piques your interest and get the latest news within the past 24 hours of BBC's coverage. 

But that's not all! Rayo understands that your time is precious, hence the news is presented in a concise, easy-to-digest format. Each headline is accompanied by a summary giving you a glimpse of the story and if you wnat more details, a direct link is provided for you to read the full article. 

Experience Rayo where the world's news meets your interest, all in one place.
''')

#Select a news category
default_url = "https://www.bbc.com"

category = st.selectbox("Select a news category of your choice",("World","Business","Politics","Health","Science & Environment","Technology","Entertainment & Arts"))
if category == "World":
    url = "https://www.bbc.com/news/world"
elif category == "Business":
    url = "https://www.bbc.com/news/business"
elif category == "Politics":
    url = "https://www.bbc.com/news/politics"
elif category == "Health":
    url = "https://www.bbc.com/news/health"
elif category == "Science & Environment":
    url = "https://www.bbc.com/news/science_and_environment"
elif category == "Technology":
    url = "https://www.bbc.com/news/technology"
elif category == "Entertainment & Arts":
    url = "https://www.bbc.com/news/entertainment_and_arts"

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

st.write("Here are the latest", category,"news headlines from BBC today")
st.table(daily_news_data['Headline News'])

#Extract Content of the news article
input_index = st.number_input("Enter the index of the news article you want to read", step = 1, min_value = 1, max_value = len(news_headlines))
story_link = daily_news_data.iloc[input_index-1]['Link']

@st.cache_data
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

full_story = full_text(story_link)

model = TFBartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)
# Generate Summary
model_result = summarizer(full_story, max_length=150, min_length=50, do_sample=False)
summarized_text = model_result[0]['summary_text']

st.button("Clear", type="primary",key=5)
if st.button('Submit',key=6):
    summary = summarizer(full_story)
    st.subheader(daily_news_data.iloc[input_index-1]['Headline News'])
    st.write(summary)
    st.link_button("Check full story", story_link)
else:
    st.empty()
