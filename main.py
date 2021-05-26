from flask import Flask, request, render_template, redirect
from math import floor
from sqlite3 import OperationalError
import string
import sqlite3
from urllib.parse import urlparse
from baseconv import base62


host = 'http://localhost:5000/'


# Base62 Encoder and Decoder
def toBase62(num):
    encoded = base62.encode(num)
    return encoded


def toBase10(text):
    decoded = base62.decode(text)
    return decoded



app = Flask(__name__)


# Home page where user should enter 
@app.route('/')
def home():
    return render_template('home.html')

#Page where short_url is displayed
@app.route('/yourShortUrl', methods=['GET', 'POST'])
def shortUrlPage():
    if request.method == 'POST':
        original_url = request.form['url']
        if urlparse(original_url).scheme == '':
            original_url = 'http://' + original_url
        
        conn = sqlite3.connect('urls.db')

        cursor = conn.cursor()
        insert_query = """ INSERT INTO WEB_URL (URL) VALUES (?)"""
        record_to_insert = (original_url,)
        cursor.execute(insert_query, record_to_insert)
        conn.commit()

        #get last inserted id
        lastrowid = cursor.lastrowid

        #encode to string
        encoded_string = toBase62(lastrowid)
        return render_template('urlPage.html', short_url= host + encoded_string)


#Redirect User to long URL when short url is entered
@app.route('/<short_url>')
def redirect_short_url(short_url):
    decoded_string = toBase10(short_url)
    redirect_url = 'http://localhost:5000'

    conn = sqlite3.connect('urls.db')

    cursor = conn.cursor()
    select_row = """SELECT url FROM WEB_URL WHERE id=?"""

    record_to_insert = (decoded_string,)

    cursor.execute(select_row, record_to_insert)

    redirect_url = cursor.fetchone()[0]
    
    return redirect(redirect_url)




if __name__ == '__main__':
    app.run(debug=True)
	


