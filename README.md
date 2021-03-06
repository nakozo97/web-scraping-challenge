# web-scraping-challenge
Web Scraping Homework - Mission to Mars

## Step 1 - Scraping

* Created a Jupyter Notebook file called `mission_to_mars.ipynb` and used this to complete my scraping and analysis tasks. The following outlines what I scraped.

### NASA Mars News

* Scraped the [NASA Mars News Site](https://mars.nasa.gov/news/) and collected the latest News Title and Paragraph Text. Assigned the text to variables. 


### JPL Mars Space Images - Featured Image

* Visited the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).

* Used splinter to navigate the site and found the image url for the current Featured Mars Image and I assigned the url string to a variable called `featured_image_url`.

### Mars Facts

* Visited the Mars Facts webpage [here](https://space-facts.com/mars/) and used Pandas to scrape the table containing the "facts" about the planet section. 

* Used Pandas to convert the data to an HTML table string.

### Mars Hemispheres

* Visited the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) and obtained high resolution images for each of the planet's hemispheres.

- - -

## Step 2 - MongoDB and Flask Application

Used MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.

* Started by converting my Jupyter notebook into a Python script called `scrape_mars.py` with a function called `scrape` that executes all of my scraping code from above and returns one Python dictionary containing all of the scraped data.

* Next, I created a route called `/scrape` and imported my `scrape_mars.py` script and called my `scrape` function.

* Stored the return values in Mongo as a Python dictionary.

* Created a root route `/` that queries my Mongo database and passes the mars data into an HTML template to display the mentioned data above.

* Created an HTML template called `index.html` that takes the mars data dictionary and displays all of the data in its appropriate HTML elements. 

* Screen shots of my final application can be found in the "images" folder. 

End of README.md