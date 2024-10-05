# !pip install webdriver-manager
# !pip install selenium

import pandas as pd
# import matplotlib.pyplot as plt

# from bs4 import BeautifulSoup
# import re
# from string import punctuation

# import nltk
# nltk.download('stopwords')
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.probability import FreqDist

# # Download the Brown corpus
# nltk.download('brown')

# from nltk.corpus import brown


# from sklearn.datasets import fetch_20newsgroups
# import seaborn as sns
# import matplotlib.pyplot as plt

# from collections import Counter
# import re

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# add in comments
def scrape_about_us_pages(about_us_urls):
    chrome_options = Options()
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)

    about_us_pages = {}

    for url in about_us_urls:
        driver.get(url)
        about_us_pages[url] = driver.page_source

    driver.quit()
    df = pd.DataFrame.from_dict(about_us_pages, orient = "index", columns = ["About Us Content"])
    df.index.name = "URL"

    return df

about_us_urls = [
    "https://www.loopnet.com/search/commercial-real-estate/logan-ut/for-lease/?sk=131c721ab08adfd4c6b0108072d7f45a&e=u"

]

scraped_df = scrape_about_us_pages(about_us_urls)