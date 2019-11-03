# main.py
from app import app

from flask import render_template, request

from sentiment import predictMood
from app import songsdata
import sys
import sqlite3 as lite

@app.route('/', methods=['GET', 'POST'])
def index():
    """
        Renders Home Page
    """
    return render_template('index.html', list_of_songs=songsdata)


@app.route('/search_results', methods=['GET', 'POST'])
def search_results():
    """
        Renders Search Results
    """
    print('we are here')
    try:
        con = lite.connect(app.config['DATABASE1'])
        cur = con.cursor()
        search_word = request.form['song_name']
        print(search_word)
        cur.execute('SELECT "text","artist","song" from "songdata_compressed" '
                    'where upper("song") is upper("'+search_word+'")')
        data = cur.fetchall()
        print(data)
        if len(data) == 0:
            print('yes')
            return render_template('not_found.html', song=search_word)

    except:
        print("Error {}:")
        sys.exit(1)
    finally:
        if con:
            con.close()
    return render_template('search_results.html', list_of_songs=data, songtitle=search_word)


@app.route('/results', methods=['GET', 'POST'])
def results():
    """
    Renders Sentiment Analysis

    """
    print('okay')
    if 'search_btn' in request.form:
        songtitle = ''
        lyrics = request.form['lyrics']
        pred, font_color, artistname, lyrics, chart_values = predictMood('', '', lyrics)
        print(pred)
        return render_template('results.html', songtitle='Unknown', font_color=font_color,
        pred=pred, artistname='Unknown', lyrics=lyrics, chart_values=chart_values)
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
        return render_template('results.html', songtitle=songtitle, font_color=font_color,
                               pred=pred, artistname=artistname, lyrics=lyrics, chart_values=chart_values)


if __name__ == '__main__':
    app.run()


