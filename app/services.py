# This file is part of the Prodeimat project
# @Author: Ricel Quispe

# handle business logic and data processing

from typing import List, Tuple, Optional
from flask import current_app
import requests
import json
from bs4 import BeautifulSoup
import os
from .database import db, delete
from .models import Article



def get_articles_from_db() -> Tuple[List[Article], int, Optional[Article]]:
    """
    Fetches all articles from the database.

    Returns:
        List[Article]
    """
     
    # check if the article post already exists to avoid duplicates
    query = db.session.query(Article)
    articles = query.all()

    return articles

def get_articles_from_json():
    articles_json_path = get_json_path('articles')

    with open(articles_json_path, 'r') as file:
        articles = json.load(file)
        
    return articles

def delete_all_articles(): 
    '''
    Delete all entries in the Article table

    '''
    db.session.execute(delete(Article))  
    db.session.commit()


def save_articles(articles):
    '''
    Store articles in the database.
    Returns: bool
    '''
    try:
        # check if table is not empty and clear all entries
        if db.session.query(Article).count() > 0:
            delete_all_articles() 

        for article in articles:
            # check if the article post already exists to avoid duplicates
            exists = db.session.query(Article.nid).filter_by(nid=article['nid']).scalar() is not None
            if not exists:
                new_article = Article(
                    nid=article['nid'],
                    title=article['title'],
                    content=article['content'],
                    link=article['link']
                )
                db.session.add(new_article)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Failed to store data: {e}")
        return False
    return True

def save_articles_as_json(articles):
    '''
    Store articles in a JSON file.
    Returns: str
    '''
    # prepare data for JSON conversion
    data_to_save = []
    for article in articles:
       
        article_data = {
            'nid': article.nid, 
            'title': article.title,
            'link': article.link,
            'content': article.content
        }
        data_to_save.append(article_data)
 
    # convert data to JSON string
    json_data = json.dumps(data_to_save, indent=4)  

    articles_json_path = get_json_path('articles')

    # write JSON data to file
    with open(articles_json_path, 'w') as json_file:
        json_file.write(json_data)

    return articles_json_path 

def get_json_path(file_name: str) -> str:
    '''
    Get the path of the JSON file
    Returns: str
    '''
    # define file path
    directory = os.path.join(current_app.static_folder, 'json')
    if not os.path.exists(directory):
        os.makedirs(directory)  # Create directory if it does not exist

    file_json_path = os.path.join(directory, file_name + '.json')
    return file_json_path


# fetch articles from API
def fetch_api_articles():
    """
    Fetches articles from a specified API URL and cleans HTML tags from the content.

    Retrieves articles via a GET request to the environment-specific DATA_URL_API. Each article's content is cleaned of HTML tags, and articles are returned with their original nid, title, link, and cleaned content.

    Returns:
        list of dict: A list of dictionaries, each containing:
            - 'nid' (str): The unique identifier of the article.
            - 'title' (str): The title of the article.
            - 'content' (str): The HTML-cleaned content of the article.
            - 'link' (str): URL link to the original article.
        Returns None if the API call fails or an exception is raised.
    """
    url = os.getenv('DATA_URL_API')
    try:
        response = requests.get(url)
        # checks the HTTP status code that was returned with the response
        response.raise_for_status()  

        # parse the JSON response
        articles = response.json()
        cleaned_articles = []

        # process each article in the response
        for article in articles:

            if 'content' in article:
                clean_text = strip_html_tags(article['content'])
                # Add cleaned text and other info to cleaned_articles
                cleaned_articles.append({
                    'nid': article['nid'],
                    'title': article['title'],
                    'content': clean_text,
                    'link': article['link']
                })
            else:
                # Handle case where no content is available
                cleaned_articles.append({
                    'nid': article['nid'],
                    'title': article['title'],
                    'content': 'No content available',
                    'link': article['link']
                })
   
        return cleaned_articles  # return the list of cleaned articles as JSON

    except requests.RequestException as e:
        print(f"Error: {e}")
        return None


# parsing html and strip HTML tags from a string
def strip_html_tags(html_content):
    '''
    Strips HTML tags from a string.
    '''
    # creates a new BeautifulSoup object 
    # argument 'html.parser' specifies the parser that BeautifulSoup should use to parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    # extracts all the text from the HTML, ignoring any tags, scripts, or styles.
    text = soup.get_text(separator=" ")
    return text
