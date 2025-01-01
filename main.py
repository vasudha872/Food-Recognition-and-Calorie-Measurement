from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from keras.models import load_model
from keras.preprocessing import image
from PIL import Image
from io import BytesIO
import numpy as np
import tensorflow as tf
from keras.utils import img_to_array , load_img
import json
import csv
import re

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Initialize SQLAlchemy engine and session
engine = create_engine('mysql+mysqldb://root:@localhost/frs')
Session = sessionmaker(bind=engine)
session = Session()

# Initialize Flask LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

# Initialize SQLAlchemy declarative base
Base = declarative_base()

# SQLAlchemy User model
class User(UserMixin, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    Pass = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

# Flask LoginManager user loader
@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))

# Index route
@app.route('/')
def index():
    """# Check if user is logged in
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    # If user is not logged in, redirect to login page
    return redirect('/login')"""
    return render_template('index.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['Uname']
        password = request.form['Pass']
        user = session.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.Pass, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['Uname']
        password = request.form['Pass']
        email = request.form['email']
        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user:
            flash('Username already exists.', 'warning')
            return redirect(url_for('signup'))
        new_user = User(username=username, Pass=generate_password_hash(password), email=email)
        session.add(new_user)
        session.commit()
        flash('Signup successful. Please log in.', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('signup.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))


# Load the pre-trained model
model = tf.keras.models.load_model('food_prediction.h5')

class_names = ['adhirasam', 'aloo_gobi', 'aloo_matar', 'aloo_methi', 'aloo_shimla_mirch', 'aloo_tikki', 'anarsa', 'ariselu', 'bandar_laddu', 'basundi', 'bhatura', 'bhindi_masala', 'biryani', 'boondi', 'butter_chicken', 'chak_hao_kheer', 'cham_cham', 'chana_masala', 'chapati', 'chhena_kheeri', 'chicken_razala', 'chicken_tikka', 'chicken_tikka_masala', 'chikki', 'daal_baati_churma', 'daal_puri', 'dal_makhani', 'dal_tadka', 'dharwad_pedha', 'doodhpak', 'double_ka_meetha', 'dum_aloo', 'gajar_ka_halwa', 'gavvalu', 'ghevar', 'gulab_jamun', 'imarti', 'jalebi', 'kachori', 'kadai_paneer', 'kadhi_pakoda', 'kajjikaya', 'kakinada_khaja', 'kalakand', 'karela_bharta', 'kofta', 'kuzhi_paniyaram', 'lassi', 'ledikeni', 'litti_chokha', 'lyangcha', 'maach_jhol', 'makki_di_roti_sarson_da_saag', 'malapua', 'misi_roti', 'misti_doi', 'modak', 'mysore_pak', 'naan', 'navrattan_korma', 'palak_paneer', 'paneer_butter_masala', 'phirni', 'pithe', 'poha', 'poornalu', 'pootharekulu', 'qubani_ka_meetha', 'rabri', 'ras_malai', 'rasgulla', 'sandesh', 'shankarpali', 'sheer_korma', 'sheera', 'shrikhand', 'sohan_halwa', 'sohan_papdi', 'sutar_feni', 'unni_appam']

# Read the CSV file and store it in a list of dictionaries
with open('indian_food.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    data = list(reader)

@app.route('/food', methods=['GET', 'POST'])
def food_recognition():
    if request.method == 'POST':
        # Read the input image file from the request
        file = request.files['food-image']
        # Load the input image using PIL
        img = Image.open(BytesIO(file.read()))
        img = img.resize((224, 224))  # Resize the image to match the input shape of the model
        x = np.array(img)
        x = np.expand_dims(x, axis=0)

        # Make a prediction using the model
        preds = model.predict(x)
        score = tf.nn.softmax(preds[0])

        class_name = class_names[np.argmax(score)]
        calorie_value = None
        # Loop through the list of dictionaries and access column values based on another column value
        for row in data:
            input_string = row['name'].lower().replace(" ", "")
            class_name_check = class_name.lower().replace("_", "")
            if(input_string == class_name_check):
                calorie_value = row['calories']
                break

        response = {
            'class_name': class_name,
            'calories': calorie_value,
            'confidence_score': 100 * np.max(score),
        }
        return render_template("food.html", response=response)

    return render_template("food.html")

@app.route('/meal_plan')
def meal_plan():
    return render_template('meal_plan.html')

@app.route('/diet')
def diet():
    return render_template('diet.html')

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(debug=True)
