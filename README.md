# Rayo
## The Ultimate News Companion
Rayo is a news summarization application that keeps you updated on the latest happenings around the World. It does this by providing you with up to date headline news and an easy-to-digest summary of news from BBC.

### Data Extraction
The applicaiton collects data from BBC using webscraping with `requests `, `beautiful soup` and `regex`

### Model
The model used for summarization is the `t5 base model` and details about the model can be found on hugging face [https://huggingface.co/t5-base](https://huggingface.co/t5-base)

![image](https://github.com/awojidetola/Rayo/assets/49078266/f5dae4e6-3db1-4124-80c6-27ed87bf8eb4)

To run the app locally, use : `streamlit run bbc_news.py` and install the required packages using the `pip install requirements.txt`

### Deployment
The app was deployed to streamlit cloud and can be accessed here: [http://bbcnewsbyrayo.streamlit.app](http://bbcnewsbyrayo.streamlit.app)
