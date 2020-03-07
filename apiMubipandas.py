import pandas as pd
import random
import math
import numpy as np
import csv
import scipy.stats
from itertools import chain
from scipy import spatial
import pickle


def cosineSimilarity(u1,u2):

    mean1 = u1['rating'].mean()
    mean2 = u2['rating'].mean()
    u1['ratingCentered'] = np.subtract(u1['rating'], mean1)
    u2['ratingCentered'] = np.subtract(u2['rating'], mean2)
    both = pd.concat([u1,u2], axis=1, join='inner')
    ratings = both['ratingCentered']
    r1 = ratings.iloc[:, [0]]
    r2 = ratings.iloc[:, [1]]
    r1 = (r1.values.tolist())
    r2 = (r2.values.tolist())
    r1 = list(chain.from_iterable(r1))
    r2 = list(chain.from_iterable(r2))
    dotproduct = sum(i[0] * i[1] for i in zip(r1, r2))
    u1sumsquares = sum(np.square(u1['ratingCentered']))**0.5
    u2sumsquares = sum(np.square(u2['ratingCentered'])) ** 0.5
    #print (u1sumsquares,' ', u2sumsquares)
    if u2sumsquares == 0:
        return(-1)
    return dotproduct/(u1sumsquares * u2sumsquares)

def naiveDistance(both):
    return 1 - (np.mean(np.absolute(np.subtract(both['rating'].iloc[:, [0]], both['rating'].iloc[:, [1]]))).item())






def estimateCloseness(both):
    ratings = both['rating']
    r1 = ratings.iloc[:, [0]]
    r2 = ratings.iloc[:, [1]]
    #print (both['rating'].head())
    #print ('Criticality is {}'.format(criticality))
    #newrating = ( both['rating'].iloc[:, [0]] / criticality)
    #print (newrating)
    #ratings['newrating'] = newrating
    #print (ratings.head())

    r1 = (r1.values.tolist())
    r2 = (r2.values.tolist())
    r1 = list(chain.from_iterable(r1))
    r2 = list(chain.from_iterable(r2))
    r1 = np.asarray(r1)
    r2 = np.asarray(r2)
    mean1 = r1.mean()
    mean2 = r2.mean()
    r1 = np.subtract(r1,mean1)
    r2 = np.subtract (r2,mean2)


    #print(r1)
    #print(r2)
    #correlation, p = scipy.stats.pearsonr(r1, r2)
    #correlation = 1 - spatial.distance.cosine(r1,r2)
    #print (correlation)
    #return correlation
    #return np.corrcoef(r1, r2)[0, 1]
    return np.mean(np.absolute(np.subtract(r1,r2))).item()
    #return np.mean(np.absolute(np.subtract(both['rating'].iloc[:, [0]], both['rating'].iloc[:, [1]]))).item()

def getSamples(both,splitAtPercent):
         # split the data set into two parts (learning and prediction), splitAtPercent % of all records and the rest
    splitPosition = int(len(
        both) * splitAtPercent / 100)  # get how many records correspond to splitAtPercent % of all records
    # firstTest = dataOfUserOfInterest[:splitPosition]
    # secondTest = dataOfUserOfInterest[splitPosition:]
    firstTestIndices = random.sample(range(len(both)),
                                     splitPosition)  # pick splitAtPosition random rows for first sample
    secondTestIndices = list(set(range(len(both))) - set(
        firstTestIndices))  # the remaining row indices go into second sample
    #print(firstTestIndices)
    #print(secondTestIndices)
    firstTest = both.iloc[firstTestIndices]  # take the splitAtPosition rows for first sample
    secondTest = both.iloc[secondTestIndices]  # and the remainder is second sample
    return firstTest, secondTest



def closeUsers(dataOfUserOfInterest, testUsers):

    #Takes in the data of a given user and the list of testUsers to compare to,
    #and returns a list of testUsers sorted by their average difference of rating of
    #commonly rated films from the given user (UserOfInterest).
    #userOfInterestFilms = dataOfUserOfInterest['film_id'].unique()  # get the films user of interest has rated
    #closeUsers = []

    df.set_index('film_id', inplace=True)
    dataOfUserOfInterest.set_index('film_id', inplace=True)


    print ('We will be testing against {} test users.'.format(len(testUsers)))
    if len(dataOfUserOfInterest) == 0: #in case we have no data for userOfInterest
        print ('No data to analyse.')
        return
    counter = 0
    closeUsers1 = []
    closeUsers2 = []
    usercounter = 0
    close = []
    for user in testUsers: #for each testUser
        counter += 1
        if counter % 1000 == 0:
            print ('Looking at testuser number {}'.format(counter))
        dataOfTestUser = df[df['user_id'] == user] #get his data

        filmsInCommon = len(set(dataOfTestUser.index.tolist()) & set(dataOfUserOfInterest.index.tolist())) #count how many films in common the users have (index is film_id)
        if filmsInCommon >= 25:
            #print ('Yay, a user with the same ratings!')
            usercounter += 1
            # dataOfTestUser.drop_duplicates(inplace=True)

            both = pd.concat([dataOfUserOfInterest, dataOfTestUser], axis=1, join='inner')
            # criticality = np.sum(both['rating'].iloc[:, [0]]) / np.sum(both['rating'].iloc[:, [1]])
            # splitAtPercent = 100
            # tests = getSamples(both, splitAtPercent)

            # test1 = tests[0]
            # test2 = tests[1]

            # testresult1 = estimateCloseness(test1)
            #averageRatingDifference1 = cosineSimilarity(dataOfUserOfInterest, dataOfTestUser)
            averageRatingDifference1 = naiveDistance(both)
            # testresult2 = estimateCloseness(test2)
            #averageRatingDifference1 = testresult1
            # averageRatingDifference2 = testresult2[0]
            # averageRatingDifference1 = estimateCloseness(test1)[0]
            # p1 = testresult1[1]
            # p2 = testresult2[1]
            # averageRatingDifference2 = estimateCloseness(test2)[0]

            # averageRatingDifference = np.mean(
            # np.absolute(np.subtract(both['rating'].iloc[:, [0]], both['rating'].iloc[:, [1]]))).item()
            # print (averageRatingDifference.item())
            username = dataOfTestUser['username'].iloc[0]  # get the username of test user (for output)
            userlink = "https://mubi.com/users/" + str(user)  # get url of test user(for output)
            if averageRatingDifference1 > 0:
                closeUsers1.append([userlink, username, averageRatingDifference1])
             #add a list consisting of tge url of testuser, username, averageRating difference and number of films in common with userOfInterest to output list
                #if averageRatingDifference2 < 1:
                    #closeUsers2.append([userlink, username, averageRatingDifference2, filmsInCommon, p2])
                #if averageRatingDifference1 < 1:
                    #print ('Average rating differences: ', usercounter)
                    #print (averageRatingDifference1)
                    #print (averageRatingDifference2)
                    #close.append([round(averageRatingDifference1,2), round(averageRatingDifference2,2), filmsInCommon, userlink])
    closeUsers1.sort(key = lambda x: x[2], reverse = True) #after all testUsers are added, sort closeUsers by average rating difference from lowest to highest (3rd element in each sublist)
    #closeUsers2.sort(key = lambda x: x[2], reverse = True)
    #close.sort(key = lambda x: x[2], reverse = True)
    print (closeUsers1) #display the sorted list of users by 'closeness' to userOfInterest
    #print (closeUsers2)
    #print (close)
    print ('The total number of users eligible for comparison was {}'.format(usercounter))
    with open("CloseUsersNaive(25+)4millionAlgirdas", "wb") as fp:  # Pickling
        pickle.dump(closeUsers1, fp)
    '''with open('CloseUsersCosine.csv', 'w') as fd:
        mubi_writer = csv.writer(fd, delimiter=',', quotechar='"',
                                 quoting=csv.QUOTE_MINIMAL)
        mubi_writer.writerow('New iteration. Split percentage is ' + str(splitAtPercent))
        mubi_writer.writerow('')
        mubi_writer.writerow(closeUsers1)  # and write that line as a row in the csv file
        mubi_writer.writerow(closeUsers2)
        mubi_writer.writerow(close)
        fd.close()'''
    return




df = pd.read_csv('APImubi_ratings10000users.csv', nrows = 1000000000, header=None) #read in scraped data from csv
df.drop_duplicates(inplace = True) #remove duplicate records (in case csv was constructed from multiple iterations of 'tester')
df.rename(columns={0: 'user_id', 1: 'username', 2: 'film_id', 3: 'film_title', 4: 'director', 5: 'year', 6: 'rating'}, inplace=True) #add sensible column names
df.dropna(subset = ['rating'], inplace = True)

print (df.tail())
df.to_csv('APImubi_ratings_with_col_4_million.csv', index=False) # save to new csv file with column names

print ('Removed nans and saved to csv')

userOfInterest = 'Algirdas Tiuninas' #pick what user we calculate 'close users' for
dataOfUserOfInterest = df[df['username'] == userOfInterest] #get that user's data
#dataOfUserOfInterest = df[df['user_id'] == 1296606]



print (dataOfUserOfInterest.head())
userOfInterestFilms = dataOfUserOfInterest['film_id'].unique() #which films has userOfInterest rated?
print (len(userOfInterestFilms))
print (userOfInterestFilms)

testUsers = df['user_id'].unique()

counter = 0
separator = 1000000
for i in testUsers[2:]:
    counter += 1
    if i > separator:
        print ('{} users before user {}'.format(counter-1,i))
        separator += 1000000


print (testUsers)
closeUsers(dataOfUserOfInterest, testUsers)





