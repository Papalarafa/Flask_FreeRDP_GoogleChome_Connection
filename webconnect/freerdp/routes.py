from flask import Blueprint,render_template,url_for,flash,redirect,request
from webconnect import app,db
from webconnect.freerdp.forms import FreeRDPForm,UpdateFreeRDPForm
from webconnect.models import ConnectionDB,FreerdpDB
import os,sys,stat
import shutil

# Blueprint object
freerdp_obj = Blueprint('freerdp',__name__,template_folder='templates')


# Build FreeRDP Commandline and Desktop file
def build_freerdp_launch_script(freerdp_conn_name:str,cmd:list):
    # FreeRDP Launch
    launch = ' '.join([str(i) for i in cmd])
    # Create working directory environment
    GET_CURRENT_USER = os.path.expanduser('~')
    CONN_PATH = GET_CURRENT_USER+"/.webconnect/"+freerdp_conn_name
    os.makedirs(CONN_PATH,exist_ok=True)
    # Create executable shell script
    with open(CONN_PATH+"/"+freerdp_conn_name+"launch.sh","w") as file:
         lines = ["#!/bin/bash\n",launch+"\n"]
         file.writelines(lines)
         file.close()
    # Change Permission
    os.chmod(CONN_PATH+"/"+freerdp_conn_name+"launch.sh",stat.S_IRUSR|stat.S_IWUSR|stat.S_IXUSR)

# Create FreeRDP Connection Desktop Shortcut
def freerdp_shortcut(freerdp_conn_name:str):
    # Create working directory environment
    GET_CURRENT_USER = os.path.expanduser('~')
    CONN_PATH = GET_CURRENT_USER+"/.webconnect/"+freerdp_conn_name
    # Create Shortcut
    with open(GET_CURRENT_USER+"/Desktop/"+freerdp_conn_name+".desktop","w") as file:
        lines = ["#!/usr/bin/env xdg-open\n","[Desktop Entry]\n","Version=1.0\n","Type=Application\n","Terminal=false\n","Exec="+CONN_PATH+"/"+freerdp_conn_name+"launch.sh\n",
        "Name="+freerdp_conn_name+"\n","Icon="+GET_CURRENT_USER+"/Desktop/freerdp.png\n","Categories=Application\n","X-Desktop-File-Install-Version=0.26"]
        file.writelines(lines)
        file.close
    # Change Permission
    os.chmod(GET_CURRENT_USER+"/Desktop/"+freerdp_conn_name+".desktop",stat.S_IRUSR|stat.S_IWUSR|stat.S_IXUSR)

# Add FreeRDP Connection
@freerdp_obj.route('/add/freerdp',methods=['GET','POST'])
def add_freerdp():
    form = FreeRDPForm()
    # Total FreeRDP Connections
    total_freerdp_conn = len(FreerdpDB.query.all())
    # Total Google Chrome Connections
    total_chrome_conn = len(ConnectionDB.query.filter_by(protocol="Google Chrome").all())

    if form.validate_on_submit():
        # FreeRDP Command List
        freerdp_cmd_list = ["xfreerdp","/cert:ignore"]
        # Check for FullScreen
        if form.resolution_fullscreen.data :
            freerdp_cmd_list.append("/f")
        # Check for Multimonitor
        if form.resolution_multimon.data:
            freerdp_cmd_list.append("/multimon")
        # Check for Span monitor
        if form.resolution_span.data:
            freerdp_cmd_list.append("/span")
        # Check for Restricted admin mode
        if form.restric_admin_mode.data:
            freerdp_cmd_list.append("/restricted-admin")
        # Check for float bar
        if form.float_bar.data:
            freerdp_cmd_list.append("/floatbar:sticky:on")
        else:
            freerdp_cmd_list.append("/floatbar:sticky:off")

        # Check for Network connection type
        match request.form.get('select-network-connection'):
            case "none":
                pass
            case "auto":
                freerdp_cmd_list.append("/network:auto")
            case "modem":
                freerdp_cmd_list.append("/network:modem")
            case "broadband-low":
                freerdp_cmd_list.append("/network:broadband-low")
            case "broadband-high":
                freerdp_cmd_list.append("/network:broadband-high")
            case "wan":
                freerdp_cmd_list.append("/network:wan")
            case "lan":
                freerdp_cmd_list.append("/network:lan")

        # Check for NLA,RDP and TLS Security
        # Check NLA
        if form.sec_nla.data:
            freerdp_cmd_list.append("+sec-nla")
        
        # Check RDP
        if form.sec_rdp.data:
            freerdp_cmd_list.append("+sec-rdp")
        
        # Check TLS
        if form.sec_tls.data:
            freerdp_cmd_list.append("+sec-tls")
        
        # Add Sound, Title and Server
        freerdp_cmd_list.append("/sound:sys:pulse")
        freerdp_cmd_list.append("/microphone:sys:pulse")
        freerdp_cmd_list.append("/t:"+form.connection_name.data)
        freerdp_cmd_list.append("/v:"+form.server_address.data)

        # Build FreeRDP Script
        build_freerdp_launch_script(form.connection_name.data,freerdp_cmd_list)
        
        # Create Shortcut
        freerdp_shortcut(form.connection_name.data)

        # Add data into Connection DB for Dashboard
        connection_db = ConnectionDB(connection_name=form.connection_name.data,address=form.server_address.data,protocol="FreeRDP")
        db.session.add(connection_db)
        db.session.commit()
        # Add data into FreeRDP DB
        freerdp_db = FreerdpDB(connection_name=form.connection_name.data,server=form.server_address.data,restricadminmode=form.restric_admin_mode.data,
        resolutionfullscreen=form.resolution_fullscreen.data,resolutionmultimon=form.resolution_multimon.data,resolutionspan=form.resolution_span.data,
        secnla=form.sec_nla.data,secrdp=form.sec_rdp.data,sectls=form.sec_tls.data,floatbar=form.float_bar.data,networkconnectiontype=request.form.get('select-network-connection'))
        db.session.add(freerdp_db)
        db.session.commit()

        # Create shortcut

        flash(f"FreeRDP connection {form.connection_name.data} created successfully",'success')
        return redirect(url_for('dashboard.dashboard'))
    return render_template('freerdp/freerdp.html',form=form,total_freerdp_conn=total_freerdp_conn,total_chrome_conn=total_chrome_conn)

# Delete FreeRDP Connection
@freerdp_obj.route('/delete/freerdp/<int:connid>',methods=['GET','POST'])
def delete_freerdp_conn(connid):
    connection_db = ConnectionDB.query.get_or_404(connid)
    freerdp_db = FreerdpDB.query.get_or_404(connid)
    # Delete connection environment dir
    GET_CURRENT_USER = os.path.expanduser('~')
    CONN_PATH = GET_CURRENT_USER+"/.webconnect/"
    COONECTION_NAME = connection_db.connection_name
    path = os.path.join(CONN_PATH,COONECTION_NAME)
    shutil.rmtree(path)
    
    # Delete Connection shortcut
    SHORTCUT_PATH = GET_CURRENT_USER+"/Desktop/"+COONECTION_NAME+".desktop"
    if os.path.exists(SHORTCUT_PATH):
        os.remove(SHORTCUT_PATH)
    
    db.session.delete(connection_db)
    db.session.delete(freerdp_db)
    db.session.commit()
    flash(f"FreeRDP connection {connection_db.connection_name} deleted successfully",'success')
    return redirect(url_for('dashboard.dashboard'))

# Edit FreeRDP Connection
@freerdp_obj.route('/edit/freerdp/<int:connid>',methods=['GET','POST'])
def edit_freerdp(connid):
    form = UpdateFreeRDPForm()
    # Total FreeRDP Connections
    total_freerdp_conn = len(FreerdpDB.query.all())
    # Total Google Chrome Connections
    total_chrome_conn = len(ConnectionDB.query.filter_by(protocol="Google Chrome").all())
    freerdp_db = FreerdpDB.query.get_or_404(connid)
    if form.validate_on_submit():
        # FreeRDP Command List
        freerdp_cmd_list = ["xfreerdp","/cert:ignore"]
        # Check for FullScreen
        if form.resolution_fullscreen.data :
            freerdp_cmd_list.append("/f")
        # Check for Multimonitor
        if form.resolution_multimon.data:
            freerdp_cmd_list.append("/multimon")
        # Check for Span monitor
        if form.resolution_span.data:
            freerdp_cmd_list.append("/span")
        # Check for Restricted admin mode
        if form.restric_admin_mode.data:
            freerdp_cmd_list.append("/restricted-admin")
        # Check for float bar
        if form.float_bar.data:
            freerdp_cmd_list.append("/floatbar:sticky:on")
        else:
            freerdp_cmd_list.append("/floatbar:sticky:off")

        # Check for Network connection type
        match request.form.get('select-network-connection'):
            case "none":
                pass
            case "auto":
                freerdp_cmd_list.append("/network:auto")
            case "modem":
                freerdp_cmd_list.append("/network:modem")
            case "broadband-low":
                freerdp_cmd_list.append("/network:broadband-low")
            case "broadband-high":
                freerdp_cmd_list.append("/network:broadband-high")
            case "wan":
                freerdp_cmd_list.append("/network:wan")
            case "lan":
                freerdp_cmd_list.append("/network:lan")

        # Check for NLA,RDP and TLS Security
        # Check NLA
        if form.sec_nla.data:
            freerdp_cmd_list.append("+sec-nla")
        else:
            freerdp_cmd_list.append("-sec-nla")

        # Check TLS
        if form.sec_tls.data:
            if "+sec-nla" in freerdp_cmd_list:
                freerdp_cmd_list[freerdp_cmd_list.index("+sec-nla")] = "-sec-nla"
            freerdp_cmd_list.append("/tls-seclevel:0")
            freerdp_cmd_list.append("/timeout:80000")
        
        # Check RDP
        if form.sec_rdp.data: 
            freerdp_cmd_list.append("+sec-rdp")
        
        
        # Add Sound, Title and Server
        freerdp_cmd_list.append("/sound:sys:pulse")
        freerdp_cmd_list.append("/microphone:sys:pulse")
        freerdp_cmd_list.append("/t:"+form.connection_name.data)
        freerdp_cmd_list.append("/v:"+form.server_address.data)

        # Build FreeRDP Script
        build_freerdp_launch_script(form.connection_name.data,freerdp_cmd_list)
        freerdp_db.server = form.server_address.data
        freerdp_db.restricadminmode = form.restric_admin_mode.data
        freerdp_db.resolutionfullscreen = form.resolution_fullscreen.data
        freerdp_db.resolutionmultimon = form.resolution_multimon.data
        freerdp_db.resolutionspan = form.resolution_span.data
        freerdp_db.secnla = form.sec_nla.data
        freerdp_db.secrdp = form.sec_rdp.data
        freerdp_db.sectls = form.sec_tls.data
        freerdp_db.floatbar = form.float_bar.data
        freerdp_db.networkconnectiontype = request.form.get('select-network-connection')
        db.session.commit()
        flash(f"FreeRDP connection {freerdp_db.connection_name} updated successfully",'success')
        return redirect(url_for('dashboard.dashboard'))
    return render_template('freerdp/edit_freerdp.html',form=form,freerdpconnection=freerdp_db,total_freerdp_conn=total_freerdp_conn,total_chrome_conn=total_chrome_conn)