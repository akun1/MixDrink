##########################################
# Get all urls from allrecipes and scrape
##########################################
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from recipe_scrapers import scrape_me
import json
import matplotlib.pyplot as plt

class adrink:
   title =""
   ingredients = []
   rating = -1
   instructions = ""

   def setTitle(self,newtitle):
      self.title = newtitle

   def setIngredients(self,newing):
      self.ingredients = newing

   def setRating(self,newr):
      self.rating = newr

   def setInstructions(self,instr):
      self.instructions = instr


class scrapeall:
   urls = []
   rawurls = []
   alckeys = ['alcohol','cocktail','vodka','tequila','schnapps','bloody-mary','margarita']
   drinks = []
   
   def geturls(self,urlstr,stopflag):
      req = requests.get(urlstr)
      htmltext = req.text
      data = req.content
      obj = BeautifulSoup(data, 'lxml')
      othersearchurls  = []
      if((obj.find_all('a',href = True) ==0) or (stopflag == 2)):
         return
      with open('cocktailsurls.txt','a') as drinkfile:
         for link in obj.find_all('a',href = True):
            if 'https://www.allrecipes.com/' in link['href'] and link['href'] not in self.rawurls:
               if any(keyword in link['href'] for keyword in self.alckeys):
                  tmpscrape = scrape_me(link['href'])
                  if(len(tmpscrape.ingredients()) > 0):
                     print("1",link['href'])
                     drinkfile.write(link['href'])
                     self.rawurls.append(link['href'])
                     self.urls.append(tmpscrape)
                  elif '/cocktails/' in link['href']:
                     othersearchurls.append(link['href'])
               else:
                  tmpreq = requests.get(link['href'])
                  tmpraw = tmpreq.content
                  alcwords = BeautifulSoup(tmpraw, 'lxml')
                  descrip = alcwords.find("meta",  property="og:description")
                  if descrip:
                     if any(keyword in descrip["content"] for keyword in self.alckeys):
                        tmpscrape = scrape_me(link['href'])
                        if(len(tmpscrape.ingredients()) > 0):
                           drinkfile.write(link['href'])
                           print("2",link['href'])
                           self.rawurls.append(link['href'])
                           self.urls.append(tmpscrape)
      
         for link in othersearchurls:
            #print(link)
            tmpreq = requests.get(link)
            tmpdata = tmpreq.content
            tmpobj = BeautifulSoup(tmpdata, 'lxml')
            for otrlink in tmpobj.find_all('a',href = True):
               #print(otrlink['href'])
               #print(otrlink)
               if 'https://www.allrecipes.com/' in otrlink['href']:
                  if otrlink['href'] not in self.rawurls:
                     if any(keyword in otrlink['href'] for keyword in self.alckeys):
                        tmpscrape = scrape_me(otrlink['href'])
                        if(len(tmpscrape.ingredients()) > 0):
                           drinkfile.write(otrlink['href'])
                           print("1",otrlink['href'])
                           self.rawurls.append(otrlink['href'])
                           self.urls.append(tmpscrape)
                     else:
                        tmpreq = requests.get(otrlink['href'])
                        tmpraw = tmpreq.content
                        alcwords = BeautifulSoup(tmpraw, 'lxml')
                        descrip = alcwords.find("meta",  property="og:description")
                        if descrip:
                           if any(keyword in descrip["content"] for keyword in self.alckeys):
                              tmpscrape = scrape_me(otrlink['href'])
                              if(len(tmpscrape.ingredients()) > 0):
                                 drinkfile.write(otrlink['href'])
                                 print("2",otrlink['href'])
                                 self.rawurls.append(otrlink['href'])
                                 self.urls.append(tmpscrape)

   
   def storeInfo(self):
      with open('cocktails.txt','a') as drinkfile:
         for drink in self.urls:
            tmping = ""
            for ing in drink.ingredients():
               tmping = tmping + ',' + ing
            line = drink.title() + '|' + tmping + '|' + drink.instructions() + '|' + drink.ratingavg() +'\n'
            drinkfile.write(line)
            tmpdrink = adrink()
            tmpdrink.setTitle(drink.title())
            tmpdrink.setIngredients(drink.ingredients())
            tmpdrink.setRating(drink.ratingavg())
            tmpdrink.setInstructions(drink.instructions())
            self.drinks.apppend(tmpdrink)

   def storeFromUrl(self):
      urls = ""
      #with open('cocktailsurls.txt','a') as drinkfile:
      urls = open('cocktailsurls.txt').read().split()
         #urls = line.split(' ')
      for url in urls:
         tmpscrape = scrape_me(url)
         tmpdrink = adrink()
         tmpdrink.setTitle(tmpscrape.title())
         tmpdrink.setIngredients(tmpscrape.ingredients())
         tmpdrink.setRating(tmpscrape.ratingavg())
         #print(tmpscrape.ratingavg())
         tmpdrink.setInstructions(tmpscrape.instructions())
         self.drinks.append(tmpdrink)


   def getratings(self,drinknames):
      print(self.rawurls)
      for name in drinknames:
         for url in self.rawurls:
            pass
         #tmpscrape = scrape_me()
         #self.urls[

   def getFileDrinks(self,fname):
      with open(fname,'a') as drinkfile:
         for line in drinkfile:
            tokens = line.split('|')
            tmpdrink = adrink()
            tmpdrink.setTitle(tokens[0])
            tmpdrink.setIngredients(tokens[1])
            tmpdrink.setInstructions(tokens[2])
            tmpdrink.setRating(tokens[3])
            self.drinks.apppend(tmpdrink)

   def runStats(self):
      ratings = []
      for drink in self.drinks:
         if float(drink.rating) > 0:
            ratings.append(float(drink.rating))
      print(len(ratings))
      #print(ratings)
      plt.plot(ratings)
      plt.xlabel('Average Ratings for Drinks')
      plt.ylabel('Stars')
      plt.show()
   
   def getFileDrinksFromUrls(self,fname):
      pass
   
   def getCocktailDB(self,fname):
      with open(fname) as json_file:
         drinks = json.load(json_file)


scrapercl = scrapeall()
#scrapercl.geturls('https://www.allrecipes.com/recipes/133/drinks/cocktails/',0)
#scrapercl.storeInfo()
scrapercl.storeFromUrl()
scrapercl.runStats()


