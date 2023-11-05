import streamlit as st
import requests
import re
import pandas as pd
import numpy as np
from datetime import datetime,timedelta
from bs4 import BeautifulSoup
import torch
from transformers import AutoTokenizer, AutoModelWithLMHead


st.set_page_config(layout="wide")
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

if category == "Science & Environment":
    class_ = 'ssrcss-1mrs5ns-PromoLink exn3ah91'

elif category == "Entertainment & Arts":
    class_ = 'ssrcss-1mrs5ns-PromoLink exn3ah91'

else:
    class_ = 'qa-heading-link lx-stream-post__header-link'
    
@st.cache_data(show_spinner=False, ttl=1800, max_entries = 10)
def extract_news(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('a',class_=class_)
    news_headlines = []
    news_links = []
    for article in articles:
        link = article.find('href')
        " ".join(article.text.split())
        news_headlines.append(article.text)
        string_soup = str(article).replace('<html><body>', '').replace('</body></html>', '').replace('<p>', '').replace('</p>', '')
        pattern = r'href="([^"]*)"'
        match = re.search(pattern, string_soup)
        if match:
            extracted_url = match.group(1)
            news_links.append(default_url + extracted_url)
        else:
            print("No match found.")
    return news_headlines, news_links

news_headlines, news_links = extract_news(url)
if category == "Science & Environment":
    news_headlines = news_headlines[:-4]
    news_links = news_links[:-4]
elif category == "Entertainment & Arts":
    news_headlines = news_headlines[:-4]
    news_links = news_links[:-4]

news_index = np.arange(1,len(news_headlines)+1)
daily_news_data = pd.DataFrame({'Headline News': news_headlines, 'Link': news_links}, index=news_index)


st.write("Here are the latest", category,"news headlines from BBC today")
output_data = pd.DataFrame({'Index': news_index, 'Headline News':news_headlines})
output_data = output_data.set_index('Index')
if output_data.empty:
    st.write ("There are no recent news in this category")
else:
    st.table(output_data)
    #Extract Content of the news article
    input_index = st.number_input("Enter the corresponding index number of the news article you want to read", step = 1, min_value = 1, max_value = len(news_headlines))
    story_link = daily_news_data.iloc[input_index-1]['Link']

@st.cache_data(show_spinner=False,ttl=1800,max_entries = 10)
def full_text(url, suppress_st_warning=True):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = ""
    for paragraph in soup.find_all('p'):
        text += paragraph.get_text() + " "
    return text

if output_data.empty:
    st.write ("Kindly select another category")
else:
    full_story = full_text(story_link)
    
@st.cache_resource(show_spinner="Loading Summary",max_entries=10)
def t5base(x):
    tokenizer=AutoTokenizer.from_pretrained('T5-base')
    model=AutoModelWithLMHead.from_pretrained('T5-base', return_dict=True)
    inputs=tokenizer.encode("sumarize: " +x,return_tensors='pt', max_length=1024, truncation=True)
    output = model.generate(inputs, min_length=50, max_length=150, do_sample=False)
    summary=tokenizer.decode(output[0], skip_special_tokens=True)
    # Capitalize first letter of summary
    summary = summary[0].upper() + summary[1:]
    # Capitalize first letter of each sentence
    summary = '. '.join([sent.capitalize() for sent in summary.split('. ')])
    return summary

if output_data.empty:
    st.write(" ")
else:
    st.button("Clear", type="primary",key=5)
    if st.button('Submit',key=6):
        our_summary = t5base(full_story)
        st.subheader(daily_news_data.iloc[input_index-1]['Headline News'])
        st.write(our_summary)
        st.link_button("Check full story", story_link)
    else:
        st.empty()
