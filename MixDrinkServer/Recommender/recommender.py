from flask import Flask
import math
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/recommendation', methods=['GET', 'POST'])
def recommendation():

    if request.json:
        input = request.json
        print(input)


    favorite_drinks = ['Cuba Libre', 'Gin and Tonic', 
        'Long Island Ice Tea', 'Espresso Martini', 'Lemon Drop',
        'Manhattan', 'Negroni', 'Mulled Wine', 'Mimosa', 'Tennessee Mud']
    
    drink_scores = {
        'Cuba Libre' : 5.0,
        'Gin and Tonic' : 4.5,
        'Long Island Ice Tea' : 4.6,
        'Espresso Martini' : 3.2,
        'Lemon Drop' : 2.9,
        'Manhattan' : 3.8,
        'Negroni' : 4.1,
        'Mulled Wine' : 1.8,
        'Mimosa' : 3.5,
        'Tennessee Mud' : 4.9
    }

    drink_confidences = {
        'Cuba Libre' : 1.0,
        'Gin and Tonic' : 0.9,
        'Long Island Ice Tea' : 0.8,
        'Espresso Martini' : 0.7,
        'Lemon Drop' : 0.6,
        'Manhattan' : 0.5,
        'Negroni' : 0.4,
        'Mulled Wine' : 0.3,
        'Mimosa' : 0.2,
        'Tennessee Mud' : 0.1
    }

    resp = simCalc(favorite_drinks)
    #for drink in drink_details:
    #    if drink['strDrink'] in favorite_drinks:
    #        drink['rating'] = drink_scores[drink['strDrink']]
    #        drink['confidence'] = drink_confidences[drink['strDrink']]
    #        resp.append(drink)
    return jsonify(resp)

#########################
# Similarity Recommender
#########################
def simCalc(favorite_drinks):
   recommended = []

   # Cluster favorite drinks
   fave_simscores = {}
   groupings =[]
   for adrink in favorite_drinks:
      adrink_scores = {}
      # find similarity between current drink and all other favorites
      for bdrink in favorite_drinks:
         if adrink != bdrink:
            adrink_scores[bdrink] = jaccScore(adrink,bdrink)
      fave_simscores[adrink] = adrink_scores
   
   # Determine groups based on similarity
   for key,val in fave_simscores.items():
      grouplist = []
      for key2,val2 in val:
         if val2 > 0.7:
            grouplist.append(key2)
      if(len(grouplist) > 0):
         grouplist.append(key)
         groupings.append(grouplist)
#WIP
   grdrinks = []
   for group in groupings:
      # Calculate similarity for each group
      groupmostsim = {}
      # Save the top ten rankings per group to make less storage
      for gdrink in group:
         for drink in drink_details:
            fav_rating = jaccScore(gdrink, drink)
            if len(groupmostsim) < 10:
               # New match
               groupmostsim[drink] = fav_rating
            else
               # Replace worse match with this one
               for key,val in groupmostsim.items:
                  if fav_rating > val:
                     del groupmostsim[key]
                     groupmostsim[drink] = fav_rating
      grdrinks.append(groupmostsim)

   # Weight most similar ratings with baseline recommendation
   baselines = baseline()
   for drinklist in grdrinks:
      for drink,score in drinklist:
         # (simscore + baseline)/ (max score + max rating)
         newscore = (score + baselines[drink])/6
         drinklist[drink] = newscore

   # Choose most similar out of each group scorelist, depending on number of groups
   groupnum = len(groupings)
   pergroup = math.floor(10/groupnum)
   for group in grdrinks:
      group_sorted = sorted(group.items(), key = operator.itemgetter(1),reverse=True)
      idx = 1
      for drink,score in group_sorted:
         recommended.append(drink)
         idx += 1
         if idx > pergroup:
            break

   return recommended


#####################
# Similarity Methods
#####################
def jaccScore(adrink, bdrink):
   intersectn = 0
   union = 0
   for ing in adrink['ingredients']:
      if ing in bdrink['ingredients']:
         intersectn += 1
      union += 1
   for ing in bdrink['ingredients']:
      if ing not in adrink['ingredients']:
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
def baseline():
   baselines = {}
   idx = 0
   mu = 0
   bx = 0
   
   # Get mu = avg
   for drink in drink_details:
      mu += drink['rating']
      idx += 1
   mu = mu/idx
   idx = 0
   # Get bx = user avg
   for drink in favorite_drinks:
      bx += drink['rating']
      idx +=1
   # Get bi = drink avg
   for drink in drink_details:
      baselines[drink] = mu + bx + drink['rating']

   return baselines

if __name__ == "__main__":

    response = requests.get('http://54.186.197.36/drinks')
    drink_details = response.json()
    print('Cataloged ' + str(len(drink_details)) + ' drinks')
    # for drink in drink_details:
    #     print(drink['strDrink'])
    app.run(host="0.0.0.0", port=80)
