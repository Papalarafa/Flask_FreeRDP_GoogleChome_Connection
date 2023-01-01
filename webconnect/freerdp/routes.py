from flask import Blueprint,render_template,url_for,flash,redirect,request
from webconnect import app,db
from webconnect.freerdp.forms import FreeRDPForm,UpdateFreeRDPForm
from webconnect.models import ConnectionDB

# Blueprint object
freerdp_obj = Blueprint('freerdp',__name__,template_folder='templates')


# Build FreeRDP Commandline and Desktop file
def freerdp_cmd():
    default_cmd = ["xfreerdp","/cert-ignore","/w:800","/h:600","/bpp:24"]
    pass

# Add FreeRDP Connection
@freerdp_obj.route('/add/freerdp',methods=['GET','POST'])
def add_freerdp():
    form = FreeRDPForm()
    # Total FreeRDP Connections
    total_freerdp_conn = len(ConnectionDB.query.filter_by(protocol="FreeRDP").all())
    # Total Google Chrome Connections
    total_chrome_conn = len(ConnectionDB.query.filter_by(protocol="Google Chrome").all())
    # FreeRDP command dict.
    freerdp_cmd_dict = {}
    if form.validate_on_submit():
        freerdp_cmd_dict["connection_name"] = form.connection_name.data
        freerdp_cmd_dict["server"] = form.server_address.data
        freerdp_cmd_dict["fullscreen"] = request.form.getlist("FullScreen")
        freerdp_cmd_dict["disablenla"] = request.form.getlist("DisableNLA")
        
        freerdp_db = ConnectionDB(connection_name=form.connection_name.data,address=form.server_address.data,protocol="FreeRDP",parameters=form.parameters.data)
        db.session.add(freerdp_db)
        db.session.commit()
        flash(f"FreeRDP connection {form.connection_name.data} created successfully",'success')
        return redirect(url_for('dashboard.dashboard'))
    return render_template('freerdp/freerdp.html',form=form,total_freerdp_conn=total_freerdp_conn,total_chrome_conn=total_chrome_conn)

# Delete FreeRDP Connection
@freerdp_obj.route('/delete/freerdp/<int:connid>',methods=['GET','POST'])
def delete_freerdp_conn(connid):
    freerdp_connection_id = ConnectionDB.query.get_or_404(connid)
    db.session.delete(freerdp_connection_id)
    db.session.commit()
    flash(f"FreeRDP connection {freerdp_connection_id.connection_name} deleted successfully",'success')
    return redirect(url_for('dashboard.dashboard'))

# Edit FreeRDP Connection
@freerdp_obj.route('/edit/freerdp/<int:connid>',methods=['GET','POST'])
def edit_freerdp(connid):
    form = UpdateFreeRDPForm()
    # Total FreeRDP Connections
    total_freerdp_conn = len(ConnectionDB.query.filter_by(protocol="FreeRDP").all())
    # Total Google Chrome Connections
    total_chrome_conn = len(ConnectionDB.query.filter_by(protocol="Google Chrome").all())
    freerdp_connection = ConnectionDB.query.get_or_404(connid)
    if form.validate_on_submit():
        freerdp_connection.connection_name = form.connection_name.data
        freerdp_connection.address = form.server_address.data
        freerdp_connection.parameters = form.parameters.data
        db.session.commit()
        flash(f"FreeRDP connection {freerdp_connection.connection_name} updated successfully",'success')
        return redirect(url_for('dashboard.dashboard'))
    return render_template('freerdp/edit_freerdp.html',form=form,freerdpconnection=freerdp_connection,total_freerdp_conn=total_freerdp_conn,total_chrome_conn=total_chrome_conn)