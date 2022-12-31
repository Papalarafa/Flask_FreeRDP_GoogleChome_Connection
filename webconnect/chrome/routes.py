from flask import Blueprint,render_template,url_for,flash,redirect,request
from webconnect import app,db
from webconnect.chrome.forms import GoogelChromeForm,UpdateGoogleChromeForm
from webconnect.models import ConnectionDB

# Blueprint object
chrome_obj = Blueprint('chrome',__name__,template_folder='templates')

# Add Google Chrome Connection
@chrome_obj.route('/add/chrome',methods=['GET','POST'])
def add_chrome():
    form = GoogelChromeForm()
    # Total FreeRDP Connections
    total_freerdp_conn = len(ConnectionDB.query.filter_by(protocol="FreeRDP").all())
    # Total Google Chrome Connections
    total_chrome_conn = len(ConnectionDB.query.filter_by(protocol="Google Chrome").all())
    if form.validate_on_submit():
        chrome_db = ConnectionDB(connection_name=form.connection_name.data,address=form.url_address.data,protocol="Google Chrome",parameters="")
        db.session.add(chrome_db)
        db.session.commit()
        flash(f"Google Chrome connection {form.connection_name.data} created successfully",'success')
        return redirect(url_for('dashboard.dashboard'))
    return render_template('chrome/chrome.html',form=form,total_freerdp_conn=total_freerdp_conn,total_chrome_conn=total_chrome_conn)


# Delete Google Chrome Connection
@chrome_obj.route('/delete/chrome/<int:connid>',methods=['GET','POST'])
def delete_chrome_conn(connid):
    chrome_connection_id = ConnectionDB.query.get_or_404(connid)
    db.session.delete(chrome_connection_id)
    db.session.commit()
    flash(f"Google Chrome connection {chrome_connection_id.connection_name} deleted successfully",'success')
    return redirect(url_for('dashboard.dashboard'))

# Edit FreeRDP Connection
@chrome_obj.route('/edit/chrome/<int:connid>',methods=['GET','POST'])
def edit_chrome(connid):
    form = UpdateGoogleChromeForm()
    # Total FreeRDP Connections
    total_freerdp_conn = len(ConnectionDB.query.filter_by(protocol="FreeRDP").all())
    # Total Google Chrome Connections
    total_chrome_conn = len(ConnectionDB.query.filter_by(protocol="Google Chrome").all())
    chrome_connection = ConnectionDB.query.get_or_404(connid)
    if form.validate_on_submit():
        chrome_connection.connection_name = form.connection_name.data
        chrome_connection.address = form.url_address.data
        db.session.commit()
        flash(f"Google Chrome connection {chrome_connection.connection_name} updated successfully",'success')
        return redirect(url_for('dashboard.dashboard'))
    return render_template('chrome/edit_chrome.html',form=form,chromeconnection=chrome_connection,total_freerdp_conn=total_freerdp_conn,total_chrome_conn=total_chrome_conn)
