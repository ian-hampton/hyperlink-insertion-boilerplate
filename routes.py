import json
import sqlite3
import uuid

from app import functions

from flask import Flask, Blueprint, render_template

app = Flask(__name__)
main = Blueprint('main', __name__)

@main.route('/')
def home():

    return render_template('index.html')

@main.route('/<url>')
def article(url):

    conn = sqlite3.connect("test.db")
    curr = conn.cursor()

    curr.execute("SELECT article_name, article_type, article_content, article_table FROM articles;")
    rows = curr.fetchall()

    article_found = False
    for row in rows:
        
        article_name = row[0]
        article_url = article_name.strip().lower().replace(" ", "_")

        if url == article_url:
            article_found = True
            article_type = row[1]
            article_contents = json.loads(row[2]) if row[2] is not None else {}
            article_table = json.loads(row[3]) if row[3] is not None else {}
            break

    if not article_found:
        return "", 404

    template_filename = f"{article_type.strip().lower()}.html"
    
    data = {
        "articleName": article_name,
        "articleContent": article_contents,
        "articleTable": article_table
    }

    links_dict = functions.create_links_dict(article_name)
    functions.insert_links(data, links_dict)

    return render_template(template_filename, data = data)
