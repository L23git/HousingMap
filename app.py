from flask import Flask, render_template
from data import Articles
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from thecraig import getalldenver
import time

app = Flask(__name__)
app.debug = True
#Sets up the Google Maps api
GoogleMaps(app, key="AIzaSyCNVF6KUM4nGz8qyqW1_aKeq82WhhLAB84")

Articles= Articles()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/map')
def map():
    #Grab denver xities
    da_marks = grab_markers('denver')
    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=39.740972,
        lng=-104.989041,
    	zoom= 13,
        style="height:620px;width:1100px;margin:0;",
        markers= da_marks
    )
    return render_template('map.html', mymap=mymap)

def grab_markers(city):
    #Get all the new Denver house listings
    new_houses = getalldenver(city)
    da_marks = list()
    for i in new_houses:
        if i['price'] > 1400:
            pindex = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
        elif i['price'] > 1200:
            pindex = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
        else:
            pindex = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
        new_mark =   {
            'icon': pindex,
            'lat': i['lat'],
            'lng': i['lon'],
            'infobox': "<a href="+i['url']+">Promising House"
            }
        da_marks.append(new_mark)
    return da_marks

@app.route('/denver')
def denver():
    #Grab denver xities
    da_marks = grab_markers('denver')
    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=39.740972,
        lng=-104.989041,
    	zoom= 13,
        style="height:620px;width:1100px;margin:0;",
        markers= da_marks
    )
    return render_template('denver.html', mymap=mymap)

@app.route('/boulder')
def boulder():
    #Grab denver xities
    da_marks = grab_markers('boulder')
    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=40.014204,
        lng=-105.270449,
    	zoom= 13,
        style="height:620px;width:1100px;margin:0;",
        markers= da_marks
    )
    return render_template('boulder.html', mymap=mymap)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles = Articles)

@app.route('/article/<string:title>/')
def article(title):
    return render_template('article.html', title=title)


if __name__ == "__main__":
    app.run()
