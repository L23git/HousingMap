# HousingMap
#Made with Flask
Runs on localhost. Pulls housing data from craiglist using an API and maps houses by their prices using the Google Maps API.

The markers that then show up on them map are color coded by the prices relative to the market. When you click on a marker the little infobox will contain a link you can click that will take you to the craiglist listing.

In thecraig.py file you can change the number of results returned. It is set at 400 with a radius of 2 miles.
