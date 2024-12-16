import os
import flask
from flask import Flask, session, render_template, request, redirect, url_for
import pickle
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'secret-key')

# Use environment variables for sensitive information
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '1234')
DB_NAME = os.environ.get('DB_NAME', 'derma')

users = {
    "rigel": generate_password_hash("password"),
    "admin": generate_password_hash("12345")
}

try:
    with open('model2.obj', 'rb') as fileObj:
        model = pickle.load(fileObj)
except FileNotFoundError:
    print("Error: Model file not found!")
    model = None

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL Platform: {e}")
        return None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/database')
def database():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try:
        with get_db_connection() as db:
            if not db:
                return "Database connection error", 500
            
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT id, name, age, sex, address, predicted_condition FROM patients")
            patients = cursor.fetchall()
            
            cursor.close()

        return render_template('database.html', patients=patients)
    except Error as e:
        print(f"Database error: {e}")
        return f"Database error: {e}", 500



@app.route('/diagnosis')
def diagnosis():
    if 'username' in session:
        return render_template('diagnosis.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Invalid username or password"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/prediction", methods=['POST', 'GET'])
def prediction():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        try:
            name = request.form.get('name')
            age = int(request.form.get('age'))
            sex = request.form.get('sex')
            address = request.form.get('address')
            
            features_list = [
                'Erythema', 'Scaling', 'definite_borders', 'itching', 'koebner_phenomenon', 
                'polygonal_papules', 'follicular_papules', 'oral_mucosal_involvement',
                'knee_and_elbow_involvement', 'scalp_involvement', 'family_history', 
                'melanin_incontinence', 'eosinophils_infiltrate', 'PNL_infiltrate',
                'fibrosis_papillary_dermis', 'exocytosis', 'acanthosis', 'hyperkeratosis', 
                'parakeratosis', 'clubbing_rete_ridges', 'elongation_rete_ridges',
                'thinning_suprapapillary_epidermis', 'spongiform_pustule', 'munro_microabcess', 
                'focal_hypergranulosis', 'disappearance_granular_layer',
                'vacuolisation_damage_basal_layer', 'spongiosis', 'saw_tooth_appearance_retes', 
                'follicular_horn_plug', 'perifollicular_parakeratosis', 
                'inflammatory_mononuclear_infiltrate', 'band_like_infiltrate'
            ]
            
            features = [int(request.form.get(feature)) for feature in features_list] + [age]
            derma = model.predict([features])

            conditions = {
                0: "Psoriasis",
                1: "Seborrheic Dermatitis",
                2: "Lichen Planus",
                3: "Pityriasis Rosea",
                4: "Chronic Dermatitis",
                5: "Pityriasis Rubra Pilaris"
            }

            result = conditions.get(derma[0], "Unknown condition")
            
            with get_db_connection() as db:
                if not db:
                    return "Database connection error", 500
                
                cursor = db.cursor()
                cursor.execute("""
                    INSERT INTO patients (name, age, sex, address, predicted_condition) 
                    VALUES (%s, %s, %s, %s, %s)""", 
                    (name, age, sex, address, result))
                
                db.commit()
                cursor.close()

            return render_template('diagnosis.html', derma=result, name=name, age=age, sex=sex, address=address)
        
        except Exception as e:
            return f"An error occurred: {e}", 500
    
    return render_template('prediction.html')



if __name__ == '__main__':
    app.run(debug=True)
