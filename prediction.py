import pandas as pd
import ast
import csv
import pickle
from statistics import mean


def exportPrediction(line0,line1,line2):
    with open('PredictionsByNaive10%(100closest)3millionSimona50users.csv', 'a') as file:
        file.write(line0)
        file.write('\n')
        file.write(line1)
        file.write('\n')
        file.write(line2)
        file.write('\n')
        file.write('\n')
    return

def exportRecommendations(recommended):
    with open('SimonaRecommendations20users.csv', 'w') as file:
        for index, val in enumerate(recommended):
            file.write('{}. {} Recommended for you. Predicted rating is {}'.format(index, val[0],val[1]))
            file.write('\n')
            file.write('\n')
            #file.write(str(i[0]) + ". Recommending " + i[1][0] + ' predicted rating')
    return



def predictRating(film, closeUsers,alldata):
    weightedAggregation = 0
    divideBy = 0
    counter = 0
    for user in closeUsers[2:30]:
        if counter == 50:
            break
        distance = 1 - user[2]
        #print (distance)
        user_id = int(user[0].split("https://mubi.com/users/")[-1])
        userRatings = alldata[alldata['user_id'] == user_id]
        if film in userRatings['film_id'].unique():
            filmline = userRatings[userRatings['film_id'] == film]
            rating = filmline['rating'].iloc[0]
            weightedAggregation += rating * distance
            divideBy += distance
            counter += 1
    if divideBy < 4:
        return None
    try:
        prediction = weightedAggregation/divideBy
    except:
        print ('No data for prediction')
        return None
    print ('Weight sum is ', divideBy)
    #print ('This is inner function rating: ', prediction)
    return prediction, counter

def getSample(closeUsers, alldata, watched):
    allfilms = {}
    for user in closeUsers[2:30]:
        distance = 1 - user[2]
        user_id = int(user[0].split("https://mubi.com/users/")[-1])
        userRatings = alldata[alldata['user_id'] == user_id]
        user_films = userRatings['film_id'].unique()
        for film in user_films:
            if film in allfilms:
                allfilms[film] += distance
            else:
                allfilms[film] = distance
    print (allfilms)
    sample = []
    for film, count in allfilms.items():
        if count > 4 and film not in watched: #if we have enough data for prediction and the user has not yet seen this film
            sample.append(film)
    print ('We have these films in our sample: {}'.format(sample))
    print ('That is {} films in total.'.format(len(sample)))
    return sample




with open("CloseUsersNaiveAgain90%2millionSimona", "rb") as fp:   # Unpickling. Other one is "CloseUsersCosineDistance", "CloseUsersPearson"
    b = pickle.load(fp)

for i in b[:20]:
    print (i)
print ('Close users total:', len(b))

df = pd.read_csv('APImubi_ratings10000users.csv', nrows = 1000000000, header=None) #read in scraped data from csv
df.drop_duplicates(inplace = True) #remove duplicate records (in case csv was constructed from multiple iterations of 'tester')
df.rename(columns={0: 'user_id', 1: 'username', 2: 'film_id', 3: 'film_title', 4: 'director', 5: 'year', 6: 'rating'}, inplace=True) #add sensible column names
df.dropna(subset = ['rating'], inplace = True)


userOfInterest = 'Algirdas Tiuninas' #pick what user we calculate 'close users' for
dataOfUserOfInterest = df[df['username'] == userOfInterest]#[:120] #get that user's data
dataOfUserOfInterest = df[df['user_id'] == 1296606]

averageRatings = df.groupby(['film_id']).mean()

mostViewed = df.groupby(['film_id']).count()
mostViewed.sort_values(by=['film_title'], ascending = False)
print (mostViewed.head(50))


#filmline = df[df['film_id'] == film]
#film_title = filmline['film_title'].iloc[0]

print (averageRatings.head())

userOfInterestFilms = dataOfUserOfInterest['film_id'].unique()

print (len(userOfInterestFilms))

allfilms = df['film_id'].unique()
sample = allfilms[:200]
sample = getSample(b, df, userOfInterestFilms)
#sample = userOfInterestFilms

print (sample)

betterThanAverage = []
offsets = []
recommended = []
usercounter = 0
filmcounter = 0
for film in sample:
    #print (film)
    filmcounter += 1
    print (filmcounter)
    filmline = df[df['film_id'] == film]
    film_title = filmline['film_title'].iloc[0]
    line0 = 'Predicting rating for ' + film_title
    print (line0)
    averageRating = averageRatings[averageRatings.index == film]['rating'].iloc[0]
    prediction = predictRating(film,b,df)
    #filmline = dataOfUserOfInterest[dataOfUserOfInterest['film_id'] == film]
    #rating = filmline['rating'].iloc[0]

    # predictionImprovement = abs(averageRating - rating) - abs(prediction[0] - rating)
    # distanceFromActual = abs(prediction[0] - rating)
    if prediction == None:
        line1 = 'No users to predict from.'
    else:
        predictionImprovement = 0
        usercounter += 1
        if prediction[0] > 1:
            recommended.append([film_title, prediction[0]])
        # line1 = ('Predicted rating is {}. Prediction based on {} users. Average rating is {}. Prediction improvement over average rating is {}.'.format(prediction[0], prediction[1], averageRating, predictionImprovement)
        # betterThanAverage.append(predictionImprovement)
        line1 = ('Predicted rating is ' + str(prediction[0]) + ' . Calculated from ' + str(prediction[1]) + ' users.')
        # offsets.append(distanceFromActual)
        # print ('Offset is ', distanceFromActual)


    print(line1)


    #line2 = ('Actual rating is ' + str(rating))
    line2 = ('Actual rating is unknown')
    print (line2)
    print ('')
    if not (line1 == 'No users to predict from.'):
        exportPrediction(line0, line1,line2)
recommended.sort(key = lambda x: x[1], reverse = True)
#print ('Average improvement over average rating is {}. Calculated from {} predictions.'.format(mean(betterThanAverage), len(betterThanAverage)))
#print ('Average prediction error is {}. Calculated from {} predictions'.format(mean(offsets), len(offsets)))
print ('In total we were able to predict {} ratings'.format(usercounter))
print ('Recommendations: ', recommended)
print ('Total {} recommendations (over 3.5 star prediction)'.format(len(recommended)))
exportRecommendations(recommended)
for i in recommended:
    print (i)




