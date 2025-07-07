from flask import Flask,Blueprint,render_template

auth_bp = Blueprint('auth',__name__,template_folder='templates')

@auth_bp.route('/login')
def login():
    return render_template('index.html')

@auth_bp.route('/logout')
def logout():
    return 'you are logged out'