from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired
from webconnect.models import ConnectionDB

# Google Chrome Connection form
class GoogelChromeForm(FlaskForm):
    connection_name = StringField('Connection Name',validators=[DataRequired()])
    url_address = StringField('Address')
    submit = SubmitField('Create')

# Update Google Chrome Connection form
class UpdateGoogleChromeForm(FlaskForm):
    connection_name = StringField('Connection Name',validators=[DataRequired()])
    url_address = StringField('Address')
    submit = SubmitField('Update')