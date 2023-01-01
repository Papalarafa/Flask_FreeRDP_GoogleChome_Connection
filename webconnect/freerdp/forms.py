from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,ValidationError
from webconnect.models import ConnectionDB

# FreeRDP Connection form
class FreeRDPForm(FlaskForm):
    connection_name = StringField('Connection Name',validators=[DataRequired()])
    server_address = StringField('Server Address',validators=[DataRequired()])
    parameters = TextAreaField('Parameters')
    submit = SubmitField('Create')

    # Check for duplicate connection name
    def validate_connection_name(self,connection_name):
        # Get FreeRDP Connection names
        freerdp_conn_names = ConnectionDB.query.filter_by(protocol="FreeRDP").all()
        for i in freerdp_conn_names:
            if i.connection_name == connection_name.data:
                raise ValidationError(f"Connection {connection_name.data} is already available.")

# Update FreeRDP Connection form
class UpdateFreeRDPForm(FlaskForm):
    connection_name = StringField('Connection Name',validators=[DataRequired()])
    server_address = StringField('Server Address',validators=[DataRequired()])
    parameters = TextAreaField('Parameters')
    submit = SubmitField('Update')