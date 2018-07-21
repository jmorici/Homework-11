# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"

mongo = PyMongo(app)


@app.route("/")
def home():

    mars = list(mongo.db.collection.find())[-1]

    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():

    mars = scrape_mars.scrape()

    mars_dict = {
        "news_title": mars["news_title"],
        "news_p": mars["news_p"],
        "featured_image_url": mars["featured_image_url"],
        "mars_weather": mars["mars_weather"],
        "table_html": mars["table_html"],
        "hemisphere_image_urls": mars["hemisphere_image_urls"]
    }

    mongo.db.collection.insert_one(mars_dict)

    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)