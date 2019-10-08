from wtforms import Form, StringField, SelectField, TextField, validators
from wtforms.validators import Required
class MusicSearchForm(Form):
    choices = [('Artist', 'Artist'),
               ('Album', 'Album'),
               ('Publisher', 'Publisher')]
    select = SelectField('Search for music:', choices=choices)
    artistname = TextField('Artist name: ', [validators.DataRequired()])
    songtitle = TextField('Song title: ', [validators.DataRequired()])
    search = StringField('')