import pandas as pd
import numpy as np
import json

HIGH_RATING = 4
MODERATE_UPPER_BOUND = 4
MODERATE_LOWER_BOUND = 3
LOW_UPPER_BOUND = 3
LOW_LOWER_BOUND = 0.5

movies = pd.read_csv("aggregate_movie_data.csv")

personality = pd.read_csv("personality-data.csv")

ratings = pd.read_csv("ratings.csv")
ratings.rename(columns={"useri": "userid", ' movie_id': 'movie_id', ' rating': 'rating'})
# Big ass dictionary
# dict[pTrait][levelOfTrait][ratingLevel][popularity][genre]

pTraits = ["openness", "conscientiousness", "extraversion", "agreeableness", "emotional_stability"]
levelOfTraits = ["lowTrait", "highTrait"]
ratingLevels = ["lowRating", "moderateRating", "highRating"]
popularityLevels = ["lowPopularity", "highPopularity"]
genres = ["is_action", "is_adventure", "is_animation", "is_children", "is_comedy",
          "is_crime", "is_documentary", "is_drama", "is_fantasy", "is_horror", "is_musical",
          "is_mystery", "is_romance", "is_science_fiction", "is_thriller", "is_war", "is_western"]

personalityAndRatingsDict = {}
for trait in pTraits:
  personalityAndRatingsDict[trait] = {}
  for levelOfTrait in levelOfTraits:
    personalityAndRatingsDict[trait][levelOfTrait] = {}
    for ratingLevel in ratingLevels:
      personalityAndRatingsDict[trait][levelOfTrait][ratingLevel] = {}
      for popularity in popularityLevels:
        personalityAndRatingsDict[trait][levelOfTrait][ratingLevel][popularity] = {}
        for genre in genres:
          personalityAndRatingsDict[trait][levelOfTrait][ratingLevel][popularity][genre] = []
          
# low <= 2 (3.5 for openness)
# high >= 6
nonOpenUsers = personality[personality[' openness'] <= 3.5]["userid"]
openUsers = personality[personality[' openness'] >= 6]["userid"]

nonConscienceUsers = personality[personality[' conscientiousness'] <= 2]["userid"]
conscienceUsers = personality[personality[' conscientiousness'] >= 6]["userid"]

nonExtravertedUsers = personality[personality[' extraversion'] <= 2]["userid"]
extravertedUsers = personality[personality[' extraversion'] >= 6]["userid"]

nonAgreeableUsers = personality[personality[' agreeableness'] <= 2]["userid"]
agreeableUsers = personality[personality[' agreeableness'] >= 6]["userid"]

nonStableUsers = personality[personality[' emotional_stability'] <= 2]["userid"]
stableUsers = personality[personality[' emotional_stability'] >= 6]["userid"]

table2Df = pd.DataFrame(data={"Personality_Trait": ["Openness",
                                                    "Conscientiousness",
                                                    "Extroversion",
                                                    "Agreeableness",
                                                    "Neuroticism"],
                              "Low_Users": [len(nonOpenUsers.index),
                                            len(nonConscienceUsers.index),
                                            len(nonExtravertedUsers.index),
                                            len(nonAgreeableUsers.index),
                                            len(nonStableUsers.index)],
                              "High_Users": [len(openUsers.index),
                                            len(conscienceUsers.index),
                                            len(extravertedUsers.index),
                                            len(agreeableUsers.index),
                                            len(stableUsers.index)]})

personalityAndUserIdDict = {
    "openness": [nonOpenUsers, openUsers],
    "conscientiousness": [nonConscienceUsers, conscienceUsers],
    "extraversion": [nonExtravertedUsers, extravertedUsers],
    "agreeableness": [nonAgreeableUsers, agreeableUsers],
    "emotional_stability": [nonStableUsers, stableUsers]
}

# movieDetails = movies[movies["movie_id"] == 7842]
# print(movieDetails)
# # isTrue = int(movieDetails["is_western"])
# print(isTrue)


# dict[pTrait][levelOfTrait][ratingLevel][popularity][genre]
count = -1
# For each trait
for trait in personalityAndUserIdDict:
  print(trait)
  # For each popularity level in each trait
  for level in personalityAndUserIdDict[trait]:
    i = 0
    count += 1
    print(count)
    print(len(level))
    # For each userId in pop level (Each user in low popularity )
    for userId in level:
      i += 1
      print(i)
      userRatings = ratings[["useri", " movie_id", " rating"]][ratings["useri"] == userId]
      # print(userRatings)
      movieIdList = userRatings[" movie_id"]
      # print(userId)
      for movie in movieIdList:
        indRating = userRatings[[" rating"]][userRatings[" movie_id"] == movie].iloc[0]
        # print(indRating)
        indRating = float(indRating.iloc[0])
        # print(indRating)
        movieDetails = movies[movies["movie_id"] == movie]
        # print("MOVIE ID", movie)
        if not movieDetails.empty:
          numOfRatings = int(movieDetails["number_of_ratings"].iloc[0])
          for genre in genres:
            isTrue = int(movieDetails.iloc[0][genre])
            if isTrue == 1:
              ratingLevel = None
              if indRating >= HIGH_RATING:
                ratingLevel = ratingLevels[2]
              elif indRating >= MODERATE_LOWER_BOUND and indRating < MODERATE_UPPER_BOUND:
                ratingLevel = ratingLevels[1]
              elif indRating >= LOW_LOWER_BOUND and indRating < LOW_UPPER_BOUND:
                ratingLevel = ratingLevels[0]
              
              if numOfRatings > 200:
                popularity = popularityLevels[1]
              else:
                popularity = popularityLevels[0]

              if ratingLevel is not None:
                personalityAndRatingsDict[trait][levelOfTraits[count % 2]][ratingLevel][popularity][genre].append(indRating)

with open('temp.json', 'w') as fp:
    json.dump(personalityAndRatingsDict, fp)

for trait in pTraits:
  for levelOfTrait in levelOfTraits:
    for ratingLevel in ratingLevels:
      for popularity in popularityLevels:
        for genre in genres:
          try:
            personalityAndRatingsDict[trait][levelOfTrait][ratingLevel][popularity][genre] = sum(personalityAndRatingsDict[trait][levelOfTrait][ratingLevel][popularity][genre]) / len(personalityAndRatingsDict[trait][levelOfTrait][ratingLevel][popularity][genre])
          except:
            personalityAndRatingsDict[trait][levelOfTrait][ratingLevel][popularity][genre] = None
with open('result.json', 'w') as fp:
    json.dump(personalityAndRatingsDict, fp)