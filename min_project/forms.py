from wtforms import Form, StringField, SelectField, TextField, TextAreaField, validators, RadioField
from wtforms.validators import Required
class MusicSearchForm(Form):
    choices = [('Artist', 'Artist'),
               ('Album', 'Album'),
               ('Publisher', 'Publisher')]
    select = RadioField('Search for music:', choices=choices)
    artistname = TextField('Artist name: ', [validators.DataRequired()])
    songtitle = TextField('Song name: ', [validators.DataRequired()])
    lyrics = TextAreaField('Post Lyrics: ', [validators.DataRequired(),
                                             validators.length(min=15)])
    search = StringField('')