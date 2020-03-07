import time
import csv
import pandas as pd
import urllib.request
import json


global exportDirectory
exportDirectory = 'APImubi_ratings10000users.csv'

def findScrapedUsers():
    global exportDirectory
    df = pd.read_csv(exportDirectory, header=None)  # read in scraped data from csv
    df.drop_duplicates(
        inplace=True)  # remove duplicate records (in case csv was constructed from multiple iterations of 'tester')
    df.rename(columns={0: 'user_id', 1: 'username', 2: 'film_title', 3: 'director', 4: 'year', 5: 'rating'},
              inplace=True)  # add sensible column names
    users = list(df['user_id'].unique())
    print('These users are already present in the file, {} of them:'.format(len(users)))
    print(users)
    return users

def scrapeData(userNo):
    scrapedUsers = findScrapedUsers()
    lastScrapedUser = max(scrapedUsers[1:])
    print ('Last scraped user: {}. Continuing with user {}'.format(lastScrapedUser, lastScrapedUser+1))
    for user in range(lastScrapedUser+1,userNo): #and for every user
        ratingurl = "https://mubi.com/services/api/ratings?user_id=" + str(user) + "&page=1&per_page=100000"
        try:
            ratingpage = urllib.request.urlopen(ratingurl)
        except:
            print('Got an error. Waiting for 30 seconds.')
            time.sleep(30)
            try:
                ratingpage = urllib.request.urlopen(ratingurl)
            except:
                print ('Failed to get url for user {}. Continuing to next iteration.'.format(user))
                continue

        text = ratingpage.read().decode('utf-8')
        if text != '[]':
            ratings = json.loads(text)
            if user % 10 == 0:
                print('We are looking at user ID', user)
            userRatings = []
            username = ratings[0].get('user').get('name')
            for j in ratings:
                rating = j.get('overall')
                film = j.get('film')
                film_id = film.get('id')
                title = film.get('title')
                year = film.get('year')
                directors = [sub['name'] for sub in film.get('directors')]
                thisRating = [user, username, film_id, title, directors, year, rating]
                userRatings.append(thisRating)
            exportRatings(userRatings)

def exportRatings(userRatings):
    global exportDirectory
    with open(exportDirectory, mode='a') as mubi_ratings: #open csv file and append this user's ratings to it
        mubi_writer = csv.writer(mubi_ratings, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for rating in userRatings:
            mubi_writer.writerow(rating)
        mubi_ratings.close()


scrapeData(5000000)
