from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Flask Configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = '878436c0a462c4145fa59eec2c43a66a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///connectiondb.db'
app.config['SQLALCHEMY_BINDS'] = {'connectiondb':'sqlite:///connectiondb.db','freerdpdb':'sqlite:///freerdpdb.db'}
db = SQLAlchemy(app)

# Import Blueprint routes object
from webconnect.dashboard.routes import dashboard_blue
from webconnect.freerdp.routes import freerdp_obj
from webconnect.chrome.routes import chrome_obj
from webconnect.install_updates.routes import installupdate_blue_obj

# Register Blueprint
app.register_blueprint(dashboard.routes.dashboard_blue,url_prefix='/')
app.register_blueprint(freerdp.routes.freerdp_obj,url_prefix='/')
app.register_blueprint(chrome.routes.chrome_obj,url_prefix='/')
app.register_blueprint(install_updates.routes.installupdate_blue_obj,url_prefix='/')