from flask import Flask, request, render_template, redirect
from math import floor
from sqlite3 import OperationalError
import string, sqlite3
from urllib.parse import urlparse
import psycopg2

host = 'http://localhost:5000/'

conn = psycopg2.connect(user="<<username>>", password="<<dbPass>>",
                        host="<<Host>>",
                        port="<<port>>",
                        database="<<dbName>>")



# Base62 Encoder and Decoder
def toBase62(num, b = 62):
    base = string.digits + string.ascii_lowercase + string.ascii_uppercase
    res= "";
    
    while (num > 0): 
        res+= base[num % b]; 
        num = int(num / b); 
        
    # Reverse the result 
    res = res[::-1] 
    return res;


def toBase10(num, b=62):
    base = string.digits + string.ascii_lowercase + string.ascii_uppercase

    llen = len(num) 
    power = 1 #Initialize power of base 
    res = 0     #Initialize result 
  
    # Decimal equivalent is str[len-1]*1 +  
    # str[len-1]*base + str[len-1]*(base^2) + ...  
    for i in range(llen - 1, -1, -1): 
          
        # A digit in input number must
        # be less than number's base  
        if (base.index(num[i])) >= b:
            print('Invalid Number!')
            break
        res += base.index(num[i]) * power 
        power = power * b
    return res



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
        
        cursor = conn.cursor()
        insert_query = """ INSERT INTO test (url) VALUES (%s) RETURNING id"""
        record_to_insert = (original_url,)
        cursor.execute(insert_query, record_to_insert)
        conn.commit()

        lastrowid = cursor.fetchone()[0]
        encoded_string = toBase62(lastrowid)
        return render_template('urlPage.html', short_url= host + encoded_string)


#Redirect User to long URL when short url is entered
@app.route('/<short_url>')
def redirect_short_url(short_url):
    decoded_string = toBase10(short_url)
    redirect_url = 'http://localhost:5000'

    cursor = conn.cursor()
    select_row = """ SELECT url FROM test WHERE id=%s """%(decoded_string)
    cursor.execute(select_row)

    redirect_url = cursor.fetchone()[0]
        
    return redirect(redirect_url)


if __name__ == '__main__':
    app.run(debug=True)
	


