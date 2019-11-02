from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()
from nltk.corpus import stopwords
import os
import sqlite3 as lite
import sys
from app import app
import matplotlib.pyplot as plt

my_dir = os.path.dirname(__file__)

DATABASE1 = os.path.join(my_dir, 'finalest.sqlite3')


app.config.from_object(__name__)

con = None
def predictMood(songtitle, artistname, lyrics):
    # try:
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
        # print(data[0][0])
        print(lyrics)
        num_positive = 0
        num_negative = 0
        num_neutral = 0
        sid = SentimentIntensityAnalyzer()
        # for i in range(len(data)):
        for sentence in lyrics:
            if sentence == ' ':
                continue
            filtered_words =[]
            for each in sentence.split():
                if each not in stopwords.words('english') and len(each) > 1 and each not in ['na','la']:
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
            else:
                num_negative += 1
        num_total = num_negative + num_neutral + num_positive
        percent_negative = (num_negative / float(num_total)) * 100
        percent_neutral = (num_neutral / float(num_total)) * 100
        percent_positive = (num_positive / float(num_total)) * 100
        lyrics = '\n'.join([each for each in lyrics])
        print(lyrics)
        if percent_negative > percent_positive:
            print('The song is sad', percent_negative)
            print('+ve',percent_positive)
            print('neutral',percent_neutral)
            # print('The song '+data[0][2]+' is sad')
            font_color = 'red'
            pred = 'sad/negative'
        elif percent_negative == percent_positive:
            font_color = 'blue'
            pred = 'mixed/neutral'
        else:
            print('The song is happy', percent_positive)
            print('-ve',percent_negative)
            print(percent_neutral)
            # print('The song '+data[0][2]+' is happy')
            font_color = 'green'
            pred = 'happy/positive'
        if by_song:
            return pred, font_color, data[0][1], lyrics, [num_positive, num_negative, num_neutral]
        else:
            return pred, font_color, '', lyrics, [num_positive, num_negative, num_neutral]
    # except:
    #
    #     print("Error {}:")
    #     sys.exit(1)
    #
    # finally:
    #     if con:
    #         con.close()
# def predictMood(songtitle, lyrics):
#     try:
#         con = lite.connect(app.config['DATABASE1'])
#         cur = con.cursor()
#         by_song = False
#         if len(songtitle) != 0 and len(lyrics) == 0:
#             cur.execute('SELECT "text","artist","song" from "songdata_compressed" where "song" is "'+songtitle+'" and ')
#             data = cur.fetchall()
#             lyrics = data[0][0].split('\n')
#             by_song = True
#         else:
#             lyrics = lyrics.split('\n')
#         # print(data[0][0])
#         print(lyrics)
#         num_positive = 0
#         num_negative = 0
#         num_neutral = 0
#         sid = SentimentIntensityAnalyzer()
#         # for i in range(len(data)):
#         for sentence in lyrics:
#             if sentence == ' ':
#                 continue
#             comp = sid.polarity_scores(sentence)
#             comp = comp['compound']
#             if comp >= 0.5:
#                 num_positive += 1
#             elif comp > -0.5 and comp < 0.5:
#                 num_neutral += 1
#             else:
#                 num_negative += 1
#         num_total = num_negative + num_neutral + num_positive
#         percent_negative = (num_negative / float(num_total)) * 100
#         percent_neutral = (num_neutral / float(num_total)) * 100
#         percent_positive = (num_positive / float(num_total)) * 100
#         lyrics = '\n'.join([each for each in lyrics])
#         print(lyrics)
#         if percent_negative > percent_positive:
#             print('The song is sad', percent_negative)
#             # print('The song '+data[0][2]+' is sad')
#             font_color = 'red'
#             pred = 'sad/negative'
#
#         else:
#             print('The song is happy', percent_positive)
#             # print('The song '+data[0][2]+' is happy')
#             font_color = 'green'
#             pred = 'happy/positive'
#         if by_song:
#             return pred, font_color, data[0][1], lyrics
#         else:
#             return pred, font_color, '', lyrics
#     except:
#
#         print("Error {}:")
#         sys.exit(1)
#
#     finally:
#         if con:
#             con.close()