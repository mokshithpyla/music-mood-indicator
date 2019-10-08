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

db = SQLAlchemy(app)