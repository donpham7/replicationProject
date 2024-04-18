import json
import pandas as pd

# Opening JSON file 
f = open('result.json') 

# returns JSON object as  
# a dictionary 
data = json.load(f) 

lowOpen = data["openness"]["lowTrait"]
highOpen = data["openness"]["highTrait"]

listOfDiffs = {}
for pTrait in data:
  for ratingLevel in data[pTrait]["lowTrait"]:
    for popularityLevel in data[pTrait]["lowTrait"][ratingLevel]:
      for genre in data[pTrait]["lowTrait"][ratingLevel][popularityLevel]:
        try:
          listOfDiffs[str(pTrait + " " + ratingLevel + " " + popularityLevel + " " + genre)] = (data[pTrait]["highTrait"][ratingLevel][popularityLevel][genre] - data[pTrait]["lowTrait"][ratingLevel][popularityLevel][genre])
        except:
          listOfDiffs[str(pTrait + " " + ratingLevel + " " + popularityLevel + " " + genre)] = -1

keysOfSortedDict = sorted(listOfDiffs, key=listOfDiffs.get, reverse=True)
for key in keysOfSortedDict:
  if "consc" in key:
    print(key, listOfDiffs[key])