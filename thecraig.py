from craigslist import CraigslistHousing
from haversine import haversine
import MySQLdb

def getalldenver(city):
    cl = CraigslistHousing(site=city, category='apa',
                         filters={'max_price': 1750, 'min_price': 20})

    results = cl.get_results(sort_by='newest', geotagged=True, limit=500)
    d = {}
    d_list = list()
    hownone = 0
    city_loc = (39.740972, -104.989041)
    if city in 'boulder':
        city_loc = (40.014204, -105.270449)
    for i in results:
        d = {}
        newprice = i['price']
        newprice = int(newprice.replace('$',''))
        d['price'] = newprice
        d['url'] = i['url']
        geoo = i['geotag']
        if geoo != None and haversine(city_loc, geoo) < 5:
            d['lat'] = geoo[0]
            d['lon'] = geoo[1]
            d_list.append(d)
    return d_list

def addToDB(city):
    conn = MySQLdb.connect(host= "localhost",
                  user="root",
                  passwd="root",
                  db="HouseMap")
    x = conn.cursor()
    cl = CraigslistHousing(site=city, category='apa',
                         filters={'max_price': 1750, 'min_price': 20})

    results = cl.get_results(sort_by='newest', geotagged=True, limit=4000)
    d = {}
    d_list = list()
    hownone = 0
    city_loc = (39.740972, -104.989041)
    if city in 'boulder':
        city_loc = (40.014204, -105.270449)
    for i in results:
        d = {}
        newprice = i['price']
        newprice = int(newprice.replace('$',''))
        d['price'] = newprice
        d['url'] = i['url']
        geoo = i['geotag']
        if geoo != None:
            radius = haversine(city_loc, geoo)
            d['lat'] = geoo[0]
            d['lon'] = geoo[1]
            d_list.append(d)
            try:
                x.execute("INSERT INTO LOCATION (city, price, lat, lon, url, radius) \
                VALUES (%s,%s, %s, %s, %s, %s)",[city, d['price'], d['lat'], d['lon'], d['url'], radius])
                conn.commit()
            except:
                conn.rollback()
    conn.close()


def main():
    addToDB('boulder')
    #newfunc()

if __name__ == "__main__":
    main()
