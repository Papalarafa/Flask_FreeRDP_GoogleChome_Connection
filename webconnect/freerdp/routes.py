from flask import Blueprint,render_template,url_for,flash,redirect,request
from webconnect import app,db
from webconnect.freerdp.forms import FreeRDPForm,UpdateFreeRDPForm
from webconnect.models import ConnectionDB
import os,sys,stat
import shutil

# Blueprint object
freerdp_obj = Blueprint('freerdp',__name__,template_folder='templates')


# Build FreeRDP Commandline and Desktop file
def build_freerdp_cmd(get_cmd:dict):
    # Create working directory environment
    GET_CURRENT_USER = os.path.expanduser('~')
    CONN_DIR = get_cmd["connection_name"]
    CONN_PATH = GET_CURRENT_USER+"/.webconnect/"+CONN_DIR
    os.makedirs(CONN_PATH,exist_ok=True)
    # Create executable shell script
    with open(CONN_PATH+"/"+CONN_DIR+".sh","w") as file:
        lines = ["#!/bin/bash\n",get_cmd["CMD"]+"\n"]
        file.writelines(lines)
        file.close()
    # Change Permission
    os.chmod(CONN_PATH+"/"+CONN_DIR+".sh",stat.S_IRWXU)

# Add FreeRDP Connection
@freerdp_obj.route('/add/freerdp',methods=['GET','POST'])
def add_freerdp():
    form = FreeRDPForm()
    # Total FreeRDP Connections
    total_freerdp_conn = len(ConnectionDB.query.filter_by(protocol="FreeRDP").all())
    # Total Google Chrome Connections
    total_chrome_conn = len(ConnectionDB.query.filter_by(protocol="Google Chrome").all())
    # FreeRDP cmd dict
    freerdp_dict = {}

    if form.validate_on_submit():
        DISPLAY = ""
        NLA = " "
        # Create FreeRDP command line
        freerdp_dict["connection_name"] = request.form.get("connection_name")
        if request.form.get("FullScreen") == "yes":
            DISPLAY = "/f"
        else:
            DISPLAY = "/w:800 /h:800"

        if request.form.get("DisableNLA") == "yes":
            NLA = "-sec-nla"
        else:
            NLA = "+sec-nla"

        cmd_str = "xfreerdp /cert-ignore /bpp:24 "+DISPLAY+" "+NLA+" /sound:sys:pulse /microphone:sys:pulse /t:"+request.form.get("connection_name")+" /v:"+request.form.get("server_address")
        freerdp_dict["CMD"] = cmd_str
        build_freerdp_cmd(freerdp_dict)

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
    # Delete connection environment dir
    GET_CURRENT_USER = os.path.expanduser('~')
    CONN_PATH = GET_CURRENT_USER+"/.webconnect/"
    COONECTION_NAME = freerdp_connection_id.connection_name
    path = os.path.join(CONN_PATH,COONECTION_NAME)
    shutil.rmtree(path)
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
        freerdp_connection.address = form.server_address.data
        freerdp_connection.parameters = form.parameters.data
        db.session.commit()
        flash(f"FreeRDP connection {freerdp_connection.connection_name} updated successfully",'success')
        return redirect(url_for('dashboard.dashboard'))
    return render_template('freerdp/edit_freerdp.html',form=form,freerdpconnection=freerdp_connection,total_freerdp_conn=total_freerdp_conn,total_chrome_conn=total_chrome_conn)