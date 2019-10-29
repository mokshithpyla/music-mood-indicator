# from flask import Flask
#
# app = Flask(__name__)
#
# @app.route('/')
# def index():
#     return 'Hello World'
#
# if __name__ == "__main__":
#     app.run(debug=True)
# app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mymusic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['WHOOSH_BASE'] = 'whoosh'
app.secret_key = "flask rocks!"

import sqlite3 as lite
import os
my_dir = os.path.dirname(__file__)

DATABASE1 = os.path.join(my_dir, 'finalest.sqlite3')


app.config.from_object(__name__)
con = lite.connect(app.config['DATABASE1'])
cur = con.cursor()
cur.execute('SELECT * from "songdata_compressed" ')
data = cur.fetchall()
print('its happening ')
con.close()
db = SQLAlchemy(app)