from places import getPlaces
import pyrebase

config = {
    "apiKey": "AIzaSyAJNPWj9EAlT1V9H-BC6xF_kJUfjxBZSuw",
    "authDomain": "dragonhacks-foodrun-app.firebaseapp.com",
    "databaseURL": "https://dragonhacks-foodrun-app.firebaseio.com",
    "projectId": "dragonhacks-foodrun-app",
    "storageBucket": "dragonhacks-foodrun-app.appspot.com",
    "messagingSenderId": "888606874417",
    "serviceAccount" : "dragonhacks-foodrun-app-firebase-adminsdk-slkcn-c49dfe9da5.json"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()
auth = firebase.auth()

from flask import *

app = Flask(__name__)
app.static_folder = "static"
user_token = None

@app.route('/')
@app.route("/login", methods=['GET','POST'])
def login():
    global user_token
    if (user_token):
        return render_template('foodrun.html')
    else:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['pass']
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                user_id = user['idToken']
                user_token = user_id
                return redirect(url_for('foodrun'))
            except:
                return render_template('login.html')

        return render_template('login.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    global user_token
    if (user_token):
        return render_template('foodrun.html')
    else:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['pass']
            try:
                auth.create_user_with_email_and_password(email, password)
                user = auth.sign_in_with_email_and_password(email, password)
                user_id = user['idToken']
                user_token = user_id
                return redirect(url_for('foodrun'))
            except:
                return render_template('index.html')

        return render_template('index.html')

@app.route("/foodrun", methods=['GET', 'POST'])
def foodrun():
    global user_token
    if (user_token):
        return render_template('foodrun.html')
    else:
        return redirect(url_for('login'))

@app.route("/driving", methods=['GET', 'POST'])
def driving():
    global user_token
    if (user_token):
        locations = getPlaces()
        if request.method == 'POST':
            restaurant = request.form['restaurantSelect']
            time = int(request.form['timeSelect'])
            data = {"restaurant" : restaurant, "time": time}
            db.child("foodEvents").push(data, user_token)
            return redirect(url_for('foodrun'))
        return render_template('driving.html', locations = locations)
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
     app.run(debug=True)

