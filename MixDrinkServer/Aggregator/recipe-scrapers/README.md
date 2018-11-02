## Running Our Scraper and/or Crawler   

The program is setup to run the scraper on the urls in the cocktailsurls.txt file.  
If you want to recollect urls from allrecipes, essentially running the crawler,  
in scrapeall.py uncomment the following line:

#scrapercl.geturls('https://www.allrecipes.com/recipes/133/drinks/cocktails/',0)

Run the scraper from the terminal from directory /MixDrink/MixDrinkServer/Aggregator/recipe-scrapers/ by typing:  
'python scrapeall.py'

This will gather the urls from the text file, scrape the recipe data, and then plot the average ratings.

## Developer Instructions for Using Recipe scraper for allrecipes.com / extended scraper  

Original project from:
git://github.com/hhursev/recipe-scrapers.git


    from recipe_scrapers import scrape_me

    # give the url as a string, it can be url from any site listed below
    scraper = scrape_me('http://allrecipes.com/Recipe/Apple-Cake-Iv/Detail.aspx')

    scraper.title()
    scraper.total_time()
    scraper.ingredients()
    scraper.instructions()
    scraper.links()
    scraper.ratingavg()

Note: scraper.links() returns a dictionary object containing all of the <a> tag attributes. The attribute names are the dictionary keys.
    
Other example in testscraperexample.py
