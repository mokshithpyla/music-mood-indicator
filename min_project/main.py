# main.py
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()
from app import app
# from db_setup import init_db, db_session

# import flask_whooshalchemy as wa
from forms import MusicSearchForm
from flask import flash, render_template, request, redirect

from sentiment import predictMood


@app.route('/', methods=['GET', 'POST'])
def index():
    search = MusicSearchForm(request.form)
    return render_template('index.html', form=search)


@app.route('/results', methods=['GET', 'POST'])
def search_results():

    form = MusicSearchForm(request.form)
    # print(request.form['tab-content'].id)
    if request.form['search_btn'] == 'Song':
        print('finding song')
        songtitle = request.form['songtitle']
        pred, font_color, artistname, lyrics = predictMood(songtitle, '')
    else:
        songtitle =''
        lyrics = request.form['lyrics']
        pred, font_color, artistname, lyrics = predictMood('', lyrics)
    return render_template('/results.html', form=form, songtitle=songtitle, font_color=font_color,
                           pred=pred, artistname=artistname, lyrics=lyrics)


if __name__ == '__main__':
    app.run()