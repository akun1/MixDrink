from recipe_scrapers import scrape_me

# give the url as a string, it can be url from any site listed below
scraper = scrape_me('https://www.allrecipes.com/recipe/147804/rum-spiked-horchata')

print(scraper.title())
scraper.total_time()
print(scraper.ingredients())
scraper.instructions()
scraper.links()
print(scraper.ratingavg())
