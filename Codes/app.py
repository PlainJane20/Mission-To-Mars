  
# Import Dependencies 
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo
import os

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.mars_db

# create instance of Flask app
app = Flask(__name__)
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_info")

# create route that renders index.html template
@app.route("/")
def home():
    mars_data = db.mars_info.find_one()
    print(mars_data)
    return render_template("index.html", mars_all= mars_data)

@app.route("/scrape")
def scrape():
     mars_dict = scrape_mars.scrape_info()
     return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)