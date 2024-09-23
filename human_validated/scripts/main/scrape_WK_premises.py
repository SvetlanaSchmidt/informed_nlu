import re
import requests
import urllib.request, sys, time
from bs4 import BeautifulSoup
import nltk
import csv
from typing import List
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

def save_news(scv_output_file: str, news_list: List[str]):
    """Saves the sentences from news articles to CSV, one per line
    Params:
     - scv_output_file path to output file
     - news_list -list of sentences from all articles from all URLs"""
    with open(scv_output_file, mode='w', newline='') as file:
        for sentence in news_list:
            file.write(sentence + '\n')
            
            
def find_dw_links(url: str):
    """Function for searching the hyperlinks from the starting URL
    When website not available returns an error
    Params:
     - url the news website http address
    Returns:
     - the list of hyperlinks leading to news articles"""   
    try:
        page=requests.get(url)      
    except Exception as e:    
        error_type, error_obj, error_info = sys.exc_info()      
        print ('Error for URL:', url)
        print (error_type, 'Line:', error_info.tb_lineno)
        
    time.sleep(2)   
    soup=BeautifulSoup(page.text,'html.parser')
    hyperlinks_to_news = []
    for link in soup.find_all("a", href=True):
        hyperlinks_to_news.append(link.get("href"))   
    return hyperlinks_to_news

def scrape_news_texts(url: str):
    """Function for extracting the text content from the news page
    0. Loads news content from the news url
    1. Parses the page content using BS Package
    2. Looks for the content of the key-tag <p> and extracts the text
    3. divides the texts into sentences and saves to a list
    Params:
     - url the hyperlink to the news article
    Return:
     - list of sentences extracted from the news page"""
  
    try:
        #add the hyperlink to the starting URL
        page=requests.get("https://www.dw.com/en/top-stories/s-9097" + url)
    except Exception as e:
        error_type, error_obj, error_info = sys.exc_info()      
        print ('Error for URL:', url)                       
        print (error_type, 'Line:', error_info.tb_lineno)
        
    time.sleep(2)   
    soup=BeautifulSoup(page.text,'html.parser')
    paragraphs = soup.find_all('p')
    content = ' '.join([para.get_text() for para in paragraphs])
    filtered_sents = []
    sentences = sent_tokenize(content)
    for sentence in sentences:
        if sentence not in filtered_sents:
            filtered_sents.append(sentence)
    return filtered_sents

def main():
    news_list = []
    url = "https://www.dw.com/en/top-stories/s-9097"
    news_links = find_dw_links(url)
    news_links.append(url) # process the text from the front news page

    #news_list = [scrape_news_texts(link) for l in news_links for link in l]

    for link in news_links:
        news_texts = scrape_news_texts(link)
        for text in news_texts:
            if text not in news_list:
                news_list.append(text)
        
    
    csv_output_file = 'news_WK_contr.csv' 
    save_news(csv_output_file, news_list)

if __name__ == "__main__":
    main()
    
