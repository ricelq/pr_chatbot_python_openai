# This file is part of the Prodeimat project
# @Author: Ricel Quispe


from flask import Blueprint, jsonify, render_template, request
from ..services import get_articles_from_json
from dotenv import load_dotenv
import os
import openai
import json


load_dotenv()


# create a Blueprint
# separation between different parts of an application, improve scalability
# by default, routes are relative to the root URL
main = Blueprint('main', __name__)
messages = []


@main.route('/chat', methods=['GET', 'POST'])
def chat():

    if request.method == 'POST':
        
        openai.api_key = os.getenv('OPENAI_API_KEY')

        try:
            messages = request.json.get('messages')
                
            articles = get_articles_from_json()

            # create a context for each article
            article_contexts = [
                {"role": "system", "content": json.dumps(article)} for article in articles
            ]            

            # add the user's messages to the context
            context_messages = article_contexts + messages

            # add some other instructions to the context messages
            context_messages.append({
                "role": "system", 
                "content": os.getenv('OPENAI_CONTEXT_INSTRUCTIONS')
            })
        
            response = openai.ChatCompletion.create(
                model=os.getenv('OPENAI_API_MODEL'), 
                messages=context_messages
            )
            return jsonify({"response": response.choices[0].message['content']})
        

        except Exception as e:
            print('Error calling OpenAI API:', str(e))
            return jsonify({"error": str(e)}), 500

    return render_template('chat.html')




