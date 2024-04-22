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
  for traitLevel in data[pTrait]:
    if traitLevel != "moderateTrait":
      for ratingLevel in data[pTrait][traitLevel]:
        for popularityLevel in data[pTrait][traitLevel][ratingLevel]:
          for genre in data[pTrait][traitLevel][ratingLevel][popularityLevel]:
            try:
              listOfDiffs[str(pTrait + " " + ratingLevel + " " + popularityLevel + " " + genre)] = abs(data[pTrait][traitLevel][ratingLevel][popularityLevel][genre] - data[pTrait]["moderateTrait"][ratingLevel][popularityLevel][genre])
            except:
              listOfDiffs[str(pTrait + " " + ratingLevel + " " + popularityLevel + " " + genre)] = -1

keysOfSortedDict = sorted(listOfDiffs, key=listOfDiffs.get, reverse=True)
for key in keysOfSortedDict:
  print(key, listOfDiffs[key])