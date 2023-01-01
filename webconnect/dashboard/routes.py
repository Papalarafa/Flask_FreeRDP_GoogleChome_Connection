from flask import Blueprint,render_template,url_for,flash,request
from webconnect import app,db
from webconnect.models import ConnectionDB

# Blueprint object
dashboard_blue = Blueprint('dashboard',__name__,template_folder='templates')

# Dashboard
@dashboard_blue.route('/',methods=['GET','POST'])
def dashboard():
    # Pagination
    page = request.args.get('page',1,type=int)
    # Total FreeRDP Connections
    total_freerdp_conn = len(ConnectionDB.query.filter_by(protocol="FreeRDP").all())
    # Total Google Chrome Connections
    total_chrome_conn = len(ConnectionDB.query.filter_by(protocol="Google Chrome").all())

    # Check the length of Connection DB
    db_len_status = ""
    if len(ConnectionDB.query.all()) == 0:
        db_len_status = "empty"
    # Connection database record
    connection_db = ConnectionDB.query.order_by(ConnectionDB.id).paginate(page=page,per_page=5)
    return render_template('dashboard/dashboard.html',dblenstatus=db_len_status,connection_db=connection_db,total_freerdp_conn=total_freerdp_conn,total_chrome_conn=total_chrome_conn)