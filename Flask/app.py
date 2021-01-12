# Import Dependencies 
from flask import Flask, render_template, redirect 
from flask_pymongo import pymongo
import scrape_mars
import os
import jinja2
import pymongo

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.mars_db

# Create an instance of Flask app
app = Flask(__name__)

# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def home(): 
# Find data
mars_info = mars.db.mars_info.find_one()

# Return template and data
return render_template("index.html", mars_all=mars_info)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 

mars_info = scrape_mars.scrape_mars_news()
mars_info = scrape_mars.scrape_mars_image()
mars_info = scrape_mars.scrape_mars_facts()
mars_info = scrape_mars.scrape_mars_hemispheres()
mars_info.update({}, mars_info, upsert=True)

return redirect("/", code=302)

if __name__ == "__main__": 
app.run(debug= True)