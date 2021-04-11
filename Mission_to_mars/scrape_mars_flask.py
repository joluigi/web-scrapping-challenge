from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_phone


app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_scrp_db")

@app.route("/")
def index():
    listings 
