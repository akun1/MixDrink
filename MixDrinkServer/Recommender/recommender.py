# test recommender for mixdrink
import math
import requests
import operator
import random
from flask import Flask, jsonify, request
#import sys
#sys.path.insert(0, '../Aggregator')
#from aggregator import get_all_cocktaildb
app = Flask(__name__)

import requests
import json

drink_details = {}

ingredient_names = ['strIngredient1','strIngredient2',
    'strIngredient3','strIngredient4','strIngredient5',
    'strIngredient6','strIngredient7','strIngredient8',
    'strIngredient9','strIngredient10','strIngredient11',
    'strIngredient12','strIngredient13','strIngredient14',
    'strIngredient15']

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/recommendation', methods=['GET', 'POST'])
def recommendation():
    drinklist = {}
    for drink in drink_details:
       drinklist[drink['strDrink']] = drink['allIngredients']

    favorite_drink_names = []
    if request.data:
        input = request.data.decode('ascii')
        input = input[1:len(input)-1]
        drink_names = input.split(',')
        favorite_drink_names = []
        for name in drink_names:
            name = name.strip()
            name = name[1:len(name)-1]
            favorite_drink_names.append(name)
        print(favorite_drink_names)
    else:
        print('Default list')
        favorite_drink_names = ['Cuba Libre', 'Gin and Tonic',
            'Long Island Ice Tea', 'Espresso Martini', 'Lemon Drop',
            'Manhattan', 'Negroni', 'Mulled Wine', 'Mimosa', 'Tennessee Mud']

    drinklist = {}
    for drink in drink_details:
       drinklist[drink['strDrink']] = drink['allIngredients']
    
    drink_scores = {}
    for drink in drink_details:
      drink_scores[drink['strDrink']] = drink['rating']

    drink_confidences = simCalc(favorite_drink_names,drink_scores,drinklist)
    resp = []
    print('RECOMMENDING: ')
    print(drink_confidences)
    for drink in drink_details:
        if drink['strDrink'] in drink_confidences:
            drink['confidence'] = drink_confidences[drink['strDrink']]
            resp.append(drink)
    #print("RECOMMENDED:")
    #print(resp)
    return jsonify(resp)

#########################
# Similarity Recommender
#########################
def simCalc(favorite_drinks,drink_scores,drinklist):
   recommended = []

   # Cluster favorite drinks
   fave_simscores = {}
   groupings =[]
   for adrink in favorite_drinks:
      adrink_scores = {}
      # find similarity between current drink and all other favorites
      for bdrink in favorite_drinks:
         if adrink != bdrink:
            if adrink in drinklist and bdrink in drinklist:
               tmpdrinka = drinklist[adrink]
               tmpdrinkb = drinklist[bdrink]
               adrink_scores[bdrink] = jaccScore(tmpdrinka,tmpdrinkb)
      fave_simscores[adrink] = adrink_scores
   
   # Determine groups based on similarity
   for key,val in fave_simscores.items():
      grouplist = []
      for key2,val2 in val.items():
         if val2 > 0.3:
            grouplist.append(key2)
      if(len(grouplist) > 0):
         grouplist.append(key)
         groupings.append(grouplist)
   # Default add all drinks as a group
   groupings.append(favorite_drinks)

   grdrinks = []
   for group in groupings:
      # Calculate similarity for each group
      groupmostsim = {}
      # Save the top ten rankings per group to make less storage
      for gdrink in group:
         for drink,val in drinklist.items():
            if drink not in favorite_drinks:
               if gdrink in drinklist:
                  gdrink_ing = drinklist[gdrink]
                  fav_rating = jaccScore(gdrink_ing, val)
                  if len(groupmostsim) < 10:
                     # New match
                     groupmostsim[drink] = fav_rating
               else:
                  tmp = ''
                  newdrink = ''
                  # Replace worse match with this one
                  for key,val in groupmostsim.items():
                     if fav_rating > val:
                        tmp = key
                        newdrink = drink
                        break
                  if newdrink != '' and newdrink not in groupmostsim:
                     groupmostsim[newdrink] = fav_rating
                     if tmp != '':
                        del groupmostsim[tmp]
      grdrinks.append(groupmostsim)

  # Get max similarity score for each drink
   jsimscores = {}
   for drink in drinklist:
      myscore = 0
      for drink2 in favorite_drinks:
         if drink2 in drinklist:
            drinking = drinklist[drink]
            drinking2 = drinklist[drink2]
            tmpscore = jaccScore(drink,drink2)
            if tmpscore > myscore:
               myscore = tmpscore
      jsimscores[drink] = myscore

   # Weight baseline ratings with sim recommendation
   baselines = baseline(drink_scores,favorite_drinks,drinklist)
   for drink, score in baselines.items():
      newscore = (score + (jsimscores[drink]*15))
      baselines[drink] = newscore

   groupnum = len(groupings)
   pergroup = math.floor(10/groupnum)
   recommended_scores = {}
   for group in grdrinks:
      group_sorted = sorted(group.items(), key = operator.itemgetter(1),reverse=True)
      idx = 1
      for drink,score in group_sorted:
         if drink not in recommended:
            #print(drink,score)
            if score < 0:
               score = -1 * score
            recommended_scores[drink] = score
            recommended.append(drink)
            idx += 1
         if idx > pergroup:
            break

   # Renormalize after biasing
   maxscore = max(baselines.items(), key=operator.itemgetter(1))[0]
   minscore = min(baselines.items(), key=operator.itemgetter(1))[0]
   for drink,score in baselines.items():
      if (baselines[maxscore]-baselines[minscore]) != 0:
         newscore = (score - baselines[minscore])/(baselines[maxscore]-baselines[minscore])
         baselines[drink] = newscore

   # Find top ten choices
   tmp = {}
   idx = 0
   baselinesort = sorted(baselines.items(), key = operator.itemgetter(1),reverse=True)
   for drink,score in baselinesort:
      if idx == 10:
         break
      if score <= 1:
         if drink not in favorite_drinks:
            tmp[drink] = score
            idx += 1

   return tmp


#####################
# Similarity Methods
#####################
def jaccScore(adrink, bdrink):
   intersectn = 0
   union = 0
   #print(adrink)
   for ing in adrink:
      if ing in bdrink:
         intersectn += 1
      union += 1
   for ing in bdrink:
      if ing not in adrink:
         union += 1
   return intersectn/union

#WIP
def cosSim(adrink,bdrink):
   numsum = 0
   densum = 0
   simscore = 0
   for ing in adrink['ingredients']:
      for ing2 in bdrink['ingredients']:
         if ing == ing2 :
            numsum += 1
            densum += 1

#######################
# Baseline recommender
#######################
def baseline(drink_scores,favorite_drinks,drinklist):
   baselines = {}
   idx = 0
   mu = 0
   bx = 0
   
   # Get mu = avg
   for drink,ing in drinklist.items():
      if drink in drink_scores:
         mu += drink_scores[drink]
         idx += 1
   mu = mu/idx
   idx = 0
   # Get bx = user avg
   for drink in favorite_drinks:
      if drink in drink_scores:
         bx += drink_scores[drink]
         idx +=1
   # Get bi = drink avg
   for drink,ing in drinklist.items():
      if drink in drink_scores:
         baselines[drink] = mu + (bx-mu) + (drink_scores[drink]-mu)

   # Normalize the baseline scores
   maxscore = max(baselines.items(), key=operator.itemgetter(1))[0]
   minscore = min(baselines.items(), key=operator.itemgetter(1))[0]
   for drink,score in baselines.items():
      #if (baselines[maxscore]-baselines[minscore]) != 0:
      newscore = (score - baselines[minscore])/(baselines[maxscore]-baselines[minscore])
      baselines[drink] = newscore
   return baselines

#########################
# Initial Recommender
#########################
# To choose drink favorites based on the quiz

# Loop through quiz answers

# Match ingredients to existing drinks
# Bail out as soon as we find ten good matches

if __name__ == "__main__":
    response = requests.get('http://54.186.197.36/drinks')
    drink_details = response.json()
    for drink in drink_details:
      drink['rating'] = random.uniform(1.0,5.0)
    #print(drink_details)
    print('Cataloged ' + str(len(drink_details)) + ' drinks')
       #print(drink['strDrink'])
    #print(drinklist)
    app.run(host="0.0.0.0", port=80)
