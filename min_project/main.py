# main.py
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()
from app import app
# from db_setup import init_db, db_session

# import flask_whooshalchemy as wa
from forms import MusicSearchForm
from flask import flash, render_template, request, redirect

from sentiment import predictMood
from app import songsdata
import sys
import sqlite3 as lite


def redirect_url(default='index'):
    return request.referrer

@app.route('/', methods=['GET', 'POST'])
def index():
    # try:
    # con = lite.connect(app.config['DATABASE1'])
    # cur = con.cursor()
    # cur.execute('SELECT * from "songdata_compressed" ')
    # data = cur.fetchall()
    search = MusicSearchForm(request.form)
    # print(d)
    return render_template('index.html', form=search, list_of_songs=songsdata)
    # except:
    #     print("Error {}:")
    #     sys.exit(1)
    # finally:
    #     if con:
    #         con.close()

@app.route('/search_results', methods=['GET', 'POST'])
def search_results():
    form = MusicSearchForm(request.form)
    # if request.form['search_btn'] == 'Search':
    print('we are here')
    try:
        con = lite.connect(app.config['DATABASE1'])
        cur = con.cursor()
        search_word = request.form['song_name']
        print(search_word)
        cur.execute('SELECT "text","artist","song" from "songdata_compressed" where upper("song") is upper("'+search_word+'")')
        data = cur.fetchall()
        print(data)
        if data == []:
            print('yes')
            return render_template('not_found.html', form=form, song=search_word)
        # if not data:
        #     cur.execute('SELECT * from "songdata_compressed"')
        #     data = cur.fetchall()
        # print(data)
    except:
        print("Error {}:")
        sys.exit(1)
    finally:
        if con:
            con.close()
    return render_template('search_results.html', form=form, list_of_songs=data, songtitle=search_word)
    # else:
    #     songtitle = ''
    #     lyrics = request.form['lyrics']
    #     print('here', lyrics)
    #     pred, font_color, artistname, lyrics = predictMood('','', lyrics)
    #     return render_template('/results.html', form=form, songtitle=songtitle, font_color=font_color,
    #                            pred=pred, artistname=artistname, lyrics=lyrics)
    #

@app.route('/results', methods=['GET', 'POST'])
def results():
    print('okay')
    form = MusicSearchForm(request.form)
    if 'search_btn' in request.form:
        songtitle = ''
        lyrics = request.form['lyrics']
        pred, font_color, artistname, lyrics, chart_values = predictMood('', '', lyrics)
        print(pred)
        return render_template('results.html', form=form, songtitle=songtitle, font_color=font_color,
        pred=pred, artistname=artistname, lyrics=lyrics, chart_values=chart_values)
    else:
        print('finding song')
        print(request.form)
        i = '0'
        for each in request.form:
            if request.form[each] == 'Analyze':
                i = each
        print(i)
        songtitle, artistname = request.form['song_details'+i].split('@')
        songtitle = songtitle.strip()
        artistname = artistname.strip()
        print(songtitle, artistname)
        pred, font_color, artistname, lyrics, chart_values = predictMood(songtitle, artistname, '')
        return render_template('results.html', form=form, songtitle=songtitle, font_color=font_color,
                               pred=pred, artistname=artistname, lyrics=lyrics, chart_values=chart_values)


if __name__ == '__main__':
    app.run()


