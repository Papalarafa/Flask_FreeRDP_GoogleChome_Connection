from flask import Blueprint,render_template,url_for,flash,request
import subprocess

# Blueprint object
installupdate_blue_obj = Blueprint('install_updates',__name__,template_folder='templates')

# Install - Update FreeRDP Google Chrome
@installupdate_blue_obj.route('/install-update',methods=['GET','POST'])
def install_update():
    # Check the installed version of Google Chrome

    return render_template('install_updates/install_updates.html')