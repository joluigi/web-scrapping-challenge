from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db_scraping"
mongo =PyMongo(app)
#mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_scrp_db")
mongo.db.mars_data.drop()


@app.route("/")
def indexroute():
    ft_img = mongo.db.mars_data.find_one()
    #latest_news = mongo.db.mars_data.find({})
    # ft_img = "https://spaceimages-mars.com/image/featured/mars2.jpg"
    output = render_template("index.html", fimage=ft_img)
    print(ft_img)
    return output

@app.route("/scrape")
def scraper():
    mars_list = scrape_mars.mars_scraping()
    mongo.db.mars_data.update({}, mars_list, upsert=True) 
    return redirect("/", code = 302)



if __name__ == "__main__":
    app.run(debug=True)