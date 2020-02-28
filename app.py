from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
#import bcrypt
import pandas as pd
import pymongo
import json

app = Flask(__name__)


mongo = pymongo.MongoClient(
    "mongodb+srv://id:pass@cluster0-bgoqd.mongodb.net/Bookify?retryWrites=true&w=majority")
db = mongo.Recomandation


@app.route('/')
def index():
    x = 0
    s = 0
    # if mongo:
    # x = pd.read_csv(
    #  "C:\\Users\\Vedanshu\\Downloads\\clean.csv")
    # records = json.loads(x.to_json(orient='records'))
    # s = db.ratings.insert_many(records)
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})

    if login_user:
        if request.form['pass'] == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashpass = request.form['pass']
            users.insert({'name': request.form['username'], 'password': hashpass,
                          'Phone_No': request.form['p_no'], 'Age': request.form['age']})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
        return render_template('index.html')
    else:
        return '<p>User already logged out</p>'


@app.route('/productsingle')
def productsingle():
    return render_template('product-single.html')


@app.route('/recommend')
def recommend():
    x = mongo.db.Recommend.find()
    return render_template('recommend.html', x=x)


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
