from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,ValidationError
from webconnect.models import ConnectionDB

# Google Chrome Connection form
class GoogelChromeForm(FlaskForm):
    connection_name = StringField('Connection Name',validators=[DataRequired()])
    url_address = StringField('Address')
    submit = SubmitField('Create')

    # Check for duplicate connection name
    def validate_connection_name(self,connection_name):
        # Get Google Chrome Connection names
        chrome_conn_names = ConnectionDB.query.filter_by(protocol="Google Chrome").all()
        for i in chrome_conn_names:
            if i.connection_name == connection_name.data:
                raise ValidationError(f"Connection {connection_name.data} is already available.")


# Update Google Chrome Connection form
class UpdateGoogleChromeForm(FlaskForm):
    connection_name = StringField('Connection Name',validators=[DataRequired()])
    url_address = StringField('Address')
    submit = SubmitField('Update')