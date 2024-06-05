# This file is part of the Prodeimat project
# @Author: Ricel Quispe

from flask import Blueprint, render_template, current_app, url_for, redirect, flash
from flask_login import current_user
import os
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import re

from ..services import get_articles_from_db, save_articles, fetch_api_articles, get_json_path, save_articles_as_json

admin = Blueprint('admin', __name__)

@admin.route('/dashboard')
def dashboard():
    '''
    Admin dashboard, display interface with some operations for the admin user.
    '''
    if is_user_admin() == False:
        return redirect(url_for('auth.login'))

    articles_json_path = get_json_path('articles')
    articles = get_articles_from_db()
    articles_count = len(articles)
    created_at = articles[0].created_at if articles else None 

    return render_template('admin/dashboard.html', articles_count=articles_count, created_at=created_at, articles_json_path=articles_json_path)

@admin.route('/statistics')
def statistics():
    '''
    Statistics interface, display interface with some charts about importing markets.
    '''
    if is_user_admin() == False:
        return redirect(url_for('auth.login'))
    
    json_path = get_json_path('exportations-suisse')

    # load data from JSON file and convert to a DataFrame
    with open(json_path, 'r') as file:
        data = json.load(file)['swiss_exports']
        df = pd.DataFrame(data)

    print(df.columns)
    # generate and save plots
    plot_urls = []
    numeric_cols = [col for col in df.columns if df[col].dtype in ['int64', 'float64']]
    for col in numeric_cols:
        # generate a URL-friendly alias
        alias = re.sub(r'[^a-zA-Z0-9]', '_', col)  
        alias = re.sub(r'__+', '_', alias)
        alias = alias.lower()
        
        # generate plot
        plt.figure()
        sns.barplot(x='Importers', y=col, data=df)
        plt.title(f"{col}")
        plt.xticks(rotation=90)
        plt.tight_layout()

        # save plot to static folder
        plot_path_abs = os.path.join(current_app.static_folder, 'img', f"{alias}.png")
        plt.savefig(plot_path_abs)

        # build plot URL
        plot_path = f"img/{alias}.png"
        plot_urls.append(plot_path)

        # close plot
        plt.close()

    return render_template('admin/statistics.html',  plot_urls=plot_urls)


@admin.route('/fetch-data')
def fetch_data():
    '''
    Fetch data from the API and store it in the database.
    '''
    if is_user_admin() == False:
        return redirect(url_for('auth.login'))

    articles = fetch_api_articles()
    
    if articles is not None:
        success = save_articles(articles)
        if success:
            flash('Data fetched and stored successfully.', 'Success')
        else:
            flash('Failed to store data.', 'Danger')
    else:
        flash('Failed to fetch data.', 'Danger')
    
    return redirect(url_for('admin.dashboard'))
    


@admin.route('/export-articles-json')
def export_articles_json():
    ''' 
    Export articles from the database to a JSON file.
    '''
    if is_user_admin() == False:
        return redirect(url_for('auth.login'))

    articles = get_articles_from_db()
    
    if articles is not None:
        file_path = save_articles_as_json(articles) 
        if file_path:
            flash('Articles were exported as JSON.', 'Success')
        else:
            flash('Failed to export articles as JSON.', 'Danger')
    else:
        flash('No articles in the database to export.', 'Danger')
    
    return redirect(url_for('admin.dashboard'))



def is_user_admin():
    '''
    Check if the current user is an admin.
    '''
    if not current_user.is_authenticated or current_user.role != 'admin':
        flash('You must be authenticated as admin!', 'Danger')
        return False
    return True
    