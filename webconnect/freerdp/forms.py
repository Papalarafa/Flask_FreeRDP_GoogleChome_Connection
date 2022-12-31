from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired
from webconnect.models import ConnectionDB

# FreeRDP Connection form
class FreeRDPForm(FlaskForm):
    connection_name = StringField('Connection Name',validators=[DataRequired()])
    server_address = StringField('Server Address',validators=[DataRequired()])
    parameters = TextAreaField('Parameters')
    submit = SubmitField('Create')

# Update FreeRDP Connection form
class UpdateFreeRDPForm(FlaskForm):
    connection_name = StringField('Connection Name',validators=[DataRequired()])
    server_address = StringField('Server Address',validators=[DataRequired()])
    parameters = TextAreaField('Parameters')
    submit = SubmitField('Update')