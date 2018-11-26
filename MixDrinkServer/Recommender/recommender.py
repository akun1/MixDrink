# test recommender for mixdrink
import math
import requests
import operator
import random
from flask import Flask,jsonify
#import sys
#sys.path.insert(0, '../Aggregator')
#from aggregator import get_all_cocktaildb
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/recommendation', methods=['GET', 'POST'])

def recommendation():
    drinklist = {}
    for drink in drink_details:
       drinklist[drink['strDrink']] = drink['allIngredients']
    #if request.json:
    #    input = request.json
    #    print(input)


    favorite_drinks = ['Cuba Libre', 'Gin and Tonic',
        'Long Island Ice Tea', 'Espresso Martini', 'Lemon Drop',
        'Manhattan', 'Negroni', 'Mulled Wine', 'Mimosa', 'Tennessee Mud']
    
    drink_scores = {}
    #drink_scores = {
    #    'Cuba Libre' : 5.0,
    #    'Gin and Tonic' : 4.5,
    #    'Long Island Ice Tea' : 4.6,
    #    'Espresso Martini' : 3.2,
    #    'Lemon Drop' : 2.9,
    #    'Manhattan' : 3.8,
    #    'Negroni' : 4.1,
    #    'Mulled Wine' : 1.8,
    #    'Mimosa' : 3.5,
    #    'Tennessee Mud' : 4.9,
    #     'Margarita' : 3.7,
    #    'Pina Colada' : 4.3,
    #    'Sparkle Wine' : 4.5
    #}
    for drink in drinklist:
      drink_scores[drink] = random.uniform(3.0,5.0)

    #drink_confidences = {
    #    'Cuba Libre' : 1.0,
    #    'Gin and Tonic' : 0.9,
    #    'Long Island Ice Tea' : 0.8,
    #    'Espresso Martini' : 0.7,
    #    'Lemon Drop' : 0.6,
    #    'Manhattan' : 0.5,
    #    'Negroni' : 0.4,
    #    'Mulled Wine' : 0.3,
    #    'Mimosa' : 0.2,
    #    'Tennessee Mud' : 0.1
    #}
    
    #print(simCalc(favorite_drinks,drink_scores,drinklist))

    drink_confidences = simCalc(favorite_drinks,drink_scores,drinklist)
    resp = []
    print('RECOMMENDING: ')
    print(drink_confidences)
    for drink in drink_details:
        if drink['strDrink'] in drink_confidences:
            drink['rating'] = drink_scores[drink['strDrink']]
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
#WIP
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

   # Weight most similar ratings with baseline recommendation
   baselines = baseline(drink_scores,favorite_drinks,drinklist)
   for drinkl in grdrinks:
      for drink,score in drinkl.items():
         newscore = (score + baselines[drink])
         drinkl[drink] = newscore

   groupnum = len(groupings)
   pergroup = math.floor(10/groupnum)
   recommended_scores = {}
   for group in grdrinks:
      group_sorted = sorted(group.items(), key = operator.itemgetter(1),reverse=True)
      idx = 1
      for drink,score in group_sorted:
         if drink not in recommended:
            #print(drink,score)
            recommended_scores[drink] = score
            recommended.append(drink)
            idx += 1
         if idx > pergroup:
            break
   #maxscore = max(recommended_scores.items(), key=operator.itemgetter(1))[0]
   #minscore = min(recommended_scores.items(), key=operator.itemgetter(1))[0]
   #normalized = {}
   #for drink,score in recommended_scores.items():
   #   normalized[drink] = (score - recommended_scores[minscore])/(recommended_scores[maxscore]-recommended_scores[minscore])

   return recommended_scores


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
         baselines[drink] = mu + bx + drink_scores[drink]

   # Normalize the baseline scores
   maxscore = max(baselines.items(), key=operator.itemgetter(1))[0]
   minscore = min(baselines.items(), key=operator.itemgetter(1))[0]
   for drink,score in baselines.items():
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

    #response = requests.get('http://54.186.197.36/drinks')
    #drinklist = response.json()
    #print('Cataloged ' + str(len(drinklist)) + ' drinks')
    # for drink in drinklist:
    #     print(drink['strDrink'])
    #drinklist = {
    #    'Cuba Libre' : ['vodka','lemon','gin'],
    #    'Gin and Tonic' : ['vodka','lemon','gin'],
    #    'Long Island Ice Tea' : ['lemon','gin','sweet tea'],
    #    'Espresso Martini' : ['espresso','gin','vodka'],
    #    'Lemon Drop' : ['lemon','gin','rum'],
    #    'Manhattan' : ['lime','vodka','licorice liquor'],
    #    'Negroni' : ['orange','vodka'],
    #    'Mulled Wine' : ['wine','gin','lime'],
    #    'Mimosa' : ['orange','juice','champagne'],
    #    'Tennessee Mud' : ['coffee liquor','vodka','espresso'],
    #    'Margarita' : ['pineapple','vodka','cherry'],
    #    'Pina Colada' : ['coconut','vodka','cherry'],
    #    'Sparkle Wine' : ['wine','champagne','cherry']
    #}
    response = requests.get('http://54.186.197.36/drinks')
    drink_details = response.json()
    #print(drink_details)
    print('Cataloged ' + str(len(drink_details)) + ' drinks')
       #print(drink['strDrink'])
    #print(drinklist)
    app.run(host="0.0.0.0", port=80)
