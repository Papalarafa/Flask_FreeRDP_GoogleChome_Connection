from flask import Blueprint,render_template,url_for,flash,redirect,request
from webconnect import app,db
from webconnect.models import ConnectionDB,FreerdpDB
import subprocess
import os
from threading import Thread
import json

# Blueprint object
launch_obj = Blueprint('launch',__name__,template_folder='templates')
status = None

# Execute Launch Script
def execute_launch_script(launch:str):
    global status
    proc = subprocess.Popen(launch,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    proc.communicate()[0]
    status = proc.pid

# Launch Connections
@launch_obj.route('/launch/<string:protocol>/<string:conn_name>/<int:connid>',methods=['GET','POST'])
def connection_launch(protocol,conn_name,connid):
    # Total FreeRDP Connections
    total_freerdp_conn = len(FreerdpDB.query.all())
    # Total Google Chrome Connections
    total_chrome_conn = len(ConnectionDB.query.filter_by(protocol="Google Chrome").all())

    # Connection Information
    protocol_name = protocol
    connection_name = conn_name
    connection_id = connid

    # Launch Connection
    # Create working directory environment
    GET_CURRENT_USER = os.path.expanduser('~')
    CONN_PATH = GET_CURRENT_USER+"/.webconnect/"+connection_name+"/"+connection_name+"launch.sh"
    t1 = Thread(target=execute_launch_script,args=(CONN_PATH,))
    t1.start()

    return render_template('launch/launch.html',protocolname=protocol_name,connectioname=connection_name,connectionid=connection_id,total_freerdp_conn=total_freerdp_conn,total_chrome_conn=total_chrome_conn)

# Status
@launch_obj.route('/status',methods=['GET'])
def getStatus():
    statusList = {'status':status}
    return json.dumps(statusList)