from flask import Blueprint,render_template,url_for,flash,request
import subprocess
import json

# Blueprint object
installupdate_blue_obj = Blueprint('install_updates',__name__,template_folder='templates')

# Install - Update FreeRDP Google Chrome
@installupdate_blue_obj.route('/install-update',methods=['GET','POST'])
def install_update():
    # Check the installed version of Google Chrome
    check_google_installed_cmd = ["which","google-chrome-stable"]
    check_google_installed_ver_cmd = ["google-chrome-stable","--version"]
    google_output = ""
    proc1 = subprocess.Popen(check_google_installed_cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    
    if len(str(proc1.communicate()[0],'UTF-8')) == 0:
        google_output = "nop"
    else:
        proc2 = subprocess.Popen(check_google_installed_ver_cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        google_output = str(proc2.communicate()[0],'UTF-8')

    # Check the installed version of FreeRDP
    check_freerdp_installed_cmd = ["which","xfreerdp"]
    check_freerdp_installed_ver_cmd = 'xfreerdp --version'
    freerdp_output = ""
    proc3 = subprocess.Popen(check_freerdp_installed_cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if len(str(proc3.communicate()[0],'UTF-8')) == 0:
        freerdp_output = "nop"
    else:
        proc4 = subprocess.Popen(check_freerdp_installed_ver_cmd,shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        freerdp_output = str(proc4.communicate()[0],'UTF-8')
    return render_template('install_updates/install_updates.html',is_google=google_output,is_freerdp=freerdp_output)