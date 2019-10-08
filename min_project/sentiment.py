from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

import sqlite3 as lite
import sys

con = None

def predictMood(songtitle):
    try:
        con = lite.connect('music_player.sqlite3')
        cur = con.cursor()
        cur.execute('SELECT "text","artist","song" from "songdata_id" where "song" is "'+songtitle+'"')
        data = cur.fetchall()
        # print(data[0][0])
        num_positive = 0
        num_negative = 0
        num_neutral = 0
        sid = SentimentIntensityAnalyzer()
        # for i in range(len(data)):
        lyrics = data[0][0].split('\n')
        for sentence in lyrics:
            if sentence == ' ':
                continue
            comp = sid.polarity_scores(sentence)
            comp = comp['compound']
            if comp >= 0.5:
                num_positive += 1
            elif comp > -0.5 and comp < 0.5:
                num_neutral += 1
            else:
                num_negative += 1
        num_total = num_negative + num_neutral + num_positive
        percent_negative = (num_negative / float(num_total)) * 100
        percent_neutral = (num_neutral / float(num_total)) * 100
        percent_positive = (num_positive / float(num_total)) * 100
        if percent_negative > percent_positive:
            # print('The song is sad', percent_negative)
            print('The song '+data[0][2]+' is sad')
            font_color = 'red'
            pred = 'sad'

        else:
            # print('The song is happy', percent_positive)
            print('The song '+data[0][2]+' is happy')
            font_color = 'green'
            pred = 'happy'
        return pred, font_color
    except:

        print("Error {}:")
        sys.exit(1)

    finally:
        if con:
            con.close()