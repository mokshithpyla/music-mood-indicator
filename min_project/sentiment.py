from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()
from nltk.corpus import stopwords
import os
import sqlite3 as lite
import sys
from app import app

my_dir = os.path.dirname(__file__)
DATABASE1 = os.path.join(my_dir, 'finalest.sqlite3')
app.config.from_object(__name__)

con = None
def predictMood(songtitle, artistname, lyrics):
    try:
        con = lite.connect(app.config['DATABASE1'])
        cur = con.cursor()
        by_song = False
        if len(lyrics) == 0:
            cur.execute('SELECT "text","artist","song" from "songdata_compressed" where "song" is "'+songtitle+'" and "artist" is "'+artistname+'"')
            data = cur.fetchall()
            lyrics = data[0][0].split('\n')
            by_song = True
        else:
            lyrics = lyrics.split('\n')
        print(lyrics)
        num_positive = 0
        num_negative = 0
        num_neutral = 0
        sid = SentimentIntensityAnalyzer()
        for sentence in lyrics:
            if sentence == ' ':
                continue
            filtered_words =[]
            for each in sentence.split():
                if each not in stopwords.words('english') and len(each) > 1 and each not in ['na', 'la']:
                    filtered_words.append(each)
                else:
                    print(each)
            final_sentence = ' '.join([each for each in filtered_words])
            comp = sid.polarity_scores(final_sentence)
            comp = comp['compound']
            if comp >= 0.5:
                num_positive += 1
            elif comp > -0.25 and comp < 0.5:
                num_neutral += 1
            # Negativity is denoted by comp in range[-inf, -0.25]
            else:
                num_negative += 1
        num_total = num_negative + num_neutral + num_positive
        percent_negative = (num_negative / float(num_total)) * 100
        percent_neutral = (num_neutral / float(num_total)) * 100
        percent_positive = (num_positive / float(num_total)) * 100
        lyrics = '\n'.join([each for each in lyrics])
        print(lyrics)
        if percent_negative > percent_positive:
            font_color = 'red'
            pred = 'sad/negative'
        elif percent_negative == percent_positive:
            font_color = 'orange'
            pred = 'mixed/neutral'
        else:
            font_color = 'blue'
            pred = 'happy/positive'
        if by_song:
            return pred, font_color, data[0][1], lyrics, [num_positive, num_negative, num_neutral]
        else:
            return pred, font_color, '', lyrics, [num_positive, num_negative, num_neutral]
    except:

        print("Error {}:")
        sys.exit(1)

    finally:
        if con:
            con.close()
