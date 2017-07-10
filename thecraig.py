from craigslist import CraigslistHousing
from haversine import haversine

def getalldenver(city):
    cl = CraigslistHousing(site=city, category='apa',
                         filters={'max_price': 1750, 'min_price': 800})

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

def main():
    getalldenver()

if __name__ == "__main__":
    main()
