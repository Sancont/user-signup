from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://user-signup:Password@localhost:8889/user-signup'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    password_2 = db.Column(db.String(20))
    email = db.Column(db.String(20))
    confirmed = db.Column(db.Boolean)

    def __init__(self,username,password,password_2, email):
        self.username = username
        self.password = password
        self.password_2 = password_2
        self.email = email
        self.confirmed = False

   
def get_not_confirmed():
    return User.query.filter_by(confirmed=False).all()

def get_confirmed():
    return User.query.filter_by(confirmed=True).all()

   
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # look inside the request to figure out what the user typed
        
        user_username = request.form['username']
        user_password = request.form['password']
        user_password_2 = request.form['password2']
        user_email = request.form['email']
        
        error_list = {}

        if (len(user_username)<3) or (len(user_username)>20) or (len(user_username)==0):
            error_list[1] = "Please specify a Username between 3-20 characters long."
                         
        
        if (len(user_password)<3) or (len(user_password)>20) or (len(user_password)==0):
            error_list[2] = "Please specify a Password between 3-20 characters long."


        
        if user_password != user_password_2:
            error_list[3] = "Passwords do not match."
    
        if user_email:
            if (len(user_email)<3) or (len(user_email)>20) or(user_email.count('@')!=1) or (user_email.count('.')!=1 or user_email.strip()==""):
                error_list[4] = "Not a valid email."
       


        if error_list:
            return render_template('signup.html', username=user_username, errorlist=error_list )

        else:
        
            username_new = User(user_username,user_password, user_password_2, user_email )
            db.session.add(username_new)
            db.session.commit()
        
            return render_template('welcome.html',title="Welcome", username=user_username)

    
    return render_template('signup.html', errorlist={} )




if __name__ == "__main__":
    app.run()
