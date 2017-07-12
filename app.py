from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import time
from functools import wraps

app = Flask(__name__)

#Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'toor'
app.config['MYSQL_DB'] = 'HouseMap'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#init MYSQL_DB
mysql = MySQL(app)


app.debug = True
#Sets up the Google Maps api
GoogleMaps(app, key="AIzaSyCNVF6KUM4nGz8qyqW1_aKeq82WhhLAB84")

@app.route('/')
def index():
    return render_template('home.html')

#Class for getting price ranges
class MapFilterForm(Form):
    upper_limit = StringField('Max Price', [validators.Length(min=1, max=6)])
    lower_limit = StringField('Min Price', [validators.Length(min=4, max=25)])

@app.route('/map')
def map():
    form = MapFilterForm(request.form)
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
    return render_template('map.html', form=form, mymap=mymap)

@app.route('/map', methods=['POST'])
def mapGetPost():
    form = MapFilterForm(request.form)
    lower_limit = int(form.lower_limit.data)
    upper_limit = int(form.upper_limit.data)
    da_marks = grab_markers('denver', lower_limit, upper_limit)
    mymap = Map(
        identifier="view-side",
        lat=39.740972,
        lng=-104.989041,
        zoom = 13,
        style="height:620px;width:1100px;margin:0;",
        markers = da_marks
    )
    return render_template('map.html', form=form, mymap=mymap)


def grab_markers(city, lower_limit=0, upper_limit=9999):
    #Get all the new Denver house
    #Create a cursor
    new_houses = []
    cur = mysql.connection.cursor()
    #Get articles
    result = cur.execute("SELECT price, url, lat, lon FROM LOCATION WHERE \
        city=%s AND radius < 6 AND price < %s AND price > %s", \
        [city, upper_limit, lower_limit])
    allinfo = cur.fetchall()
    da_marks = list()
    for i in allinfo:
        if i['price'] > 1600:
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

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/select')
def select():
    #Create a cursor
    cur = mysql.connection.cursor()
    #Get articles
    result = cur.execute("SELECT DISTINCT city FROM LOCATION")
    cities = cur.fetchall()
    cityHolder = [i['city'] for i in cities]
    if result > 0:
        return render_template('select.html', cities=cityHolder)
    else:
        msg = 'No Houses found'
        return render_template('select.html', msg=msg)
    cur.close()

@app.route('/city/<string:city>/', methods=['GET', 'POST'])
def citylink(city):
    if request.method == 'POST':
        form = MapFilterForm(request.form)
        lower_limit = int(form.lower_limit.data)
        upper_limit = int(form.upper_limit.data)
        da_marks = grab_markers(city, lower_limit, upper_limit)
        city_coords = getCityCoord(city)
        mymap = Map(
            identifier="view-side",
            lat=city_coords[0],
            lng=city_coords[1],
            zoom = 13,
            style="height:620px;width:1100px;margin:0;",
            markers = da_marks
        )
        return render_template('city.html', form=form, cityP = city, mymap=mymap)
    else:
        form = MapFilterForm(request.form)
        #Grab xities
        da_marks = grab_markers(city)
        city_coords = getCityCoord(city)
        # creating a map in the view
        mymap = Map(
            identifier="view-side",
            lat=city_coords[0],
            lng=city_coords[1],
    	    zoom= 13,
            style="height:620px;width:1100px;margin:0;",
            markers= da_marks
        )
        return render_template('city.html', cityP=city, form=form, mymap=mymap)

def getCityCoord(city):
    city_key = {}
    city_key['denver'] = (39.740972, -104.989041)
    city_key['boulder'] = (40.014204, -105.270449)
    return city_key[city]
@app.route('/articles')
def articles():
    #Create a cursor
    cur = mysql.connection.cursor()
    #Get articles
    result = cur.execute("SELECT * FROM ARTICLES")
    articles = cur.fetchall()

    if result > 0:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No Aerticles found'
        return render_template('articles.html', msg=msg)
    cur.close()

@app.route('/article/<string:id>/')
def article(id):
    #Create a cursor
    cur = mysql.connection.cursor()
    #Get articles
    result = cur.execute("SELECT * FROM ARTICLES WHERE id= %s", [id])
    article = cur.fetchone()
    return render_template('article.html', article=article)

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message="Passwords do not match")
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        #Create the cursor
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO USERS(name, email, username, password) VALUES \
                    (%s, %s, %s, %s)", (name, email, username, password))
        #commit to db
        mysql.connection.commit()

        #Close the connection
        cur.close()
        flash("You are now registered")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

#User logging
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # GEt Form fFields
        username = request.form['username']
        password_candidate = request.form['password']

        # Cursor to the dB
        cur = mysql.connection.cursor()

        #Get user by username
        result = cur.execute("SELECT * FROM USERS WHERE username= %s", [username])

        if result > 0:
            #get the hashed password
            data = cur.fetchone()
            password = data['password']

            #Compare the Passwords
            if sha256_crypt.verify(password_candidate, password):
                #Passed
                session['logged_in'] = True
                session['username'] = username

                flash("You are now logge in", 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Username not found'
                return render_template('login.html', error=error)
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)
    return render_template('login.html')
#Check if user is logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

#logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash("You are now logged out", 'success')
    return render_template('login.html')

@app.route('/dashboard')
@is_logged_in
def dashboard():
    #Create a cursor
    cur = mysql.connection.cursor()
    #Get articles
    result = cur.execute("SELECT * FROM ARTICLES")
    articles = cur.fetchall()

    if result > 0:
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No Aerticles found'
        return render_template('dashboard.html', msg=msg)
    cur.close()

class ArticleForm(Form):
    title = StringField('Ttile', [validators.Length(min=1, max=250)])
    body = TextAreaField('Body', [validators.Length(min=30)])

@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.title.data
        #Create cursor
        cur = mysql.connection.cursor()
        #execute
        cur.execute("INSERT INTO ARTICLES(title, body, author) VALUES (%s, %s, %s)", (title, body, session['username']))
        #Commit to db
        mysql.connection.commit()
        #close connection
        cur.close()

        flash("Article created", 'success')

        return redirect(url_for('dashboard'))
    return render_template('add_article.html', form=form)

@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    #Create cursor
    cur = mysql.connection.cursor()
    #Get the article by id
    result = cur.execute("SELECT * FROM ARTICLES WHERE id=%s", [id])
    article = cur.fetchone()

    #Get form
    form = ArticleForm(request.form)
    #populate the fFields
    form.title.data = article['title']
    form.body.data = article['body']
    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']
        #Create cursor
        cur = mysql.connection.cursor()
        #execute
        cur.execute("UPDATE ARTICLES SET title=%s, body=%s WHERE id = %s", (title, body, id))
        #Commit to db
        mysql.connection.commit()
        #close connection
        cur.close()

        flash("Article created", 'success')

        return redirect(url_for('dashboard'))
    return render_template('edit_article.html', form=form)

@app.route('/delete_article/<string:id>', methods=["POST"])
@is_logged_in
def delete_article(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM ARTICLES WHERE id=%s", [id])
    mysql.connection.commit()
    cur.close()
    flash("Article Dellete", 'succes')


if __name__ == "__main__":
    app.secret_key = 'secret123'
    app.run()
