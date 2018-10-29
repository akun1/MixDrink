## Recipe scraper for allrecipes.com

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
