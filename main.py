import flask
from flask import Flask, session, render_template, request, redirect, url_for
import pickle  
import sqlite3

app = Flask(__name__)
app.secret_key = "secret-key"

users = {
    "rigel": "password",
    "admin": "12345"
}

fileObj = open('model2.obj', 'rb')
model = pickle.load(fileObj)

# Set up SQLite
db = sqlite3.connect('derma.db', check_same_thread=False)
db.row_factory = sqlite3.Row  

cursor = db.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        name TEXT,
        age INTEGER,
        sex TEXT,
        address TEXT,
        predicted_condition TEXT
    )
''')
db.commit()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/database')
def database():
    if 'username' in session:
        cursor = db.cursor()
        cursor.execute("SELECT id, name, age, sex, address, predicted_condition FROM patients WHERE username = ?", (session['username'],))
        patients = cursor.fetchall()
        return render_template('database.html', patients=patients)
    
    return redirect(url_for('login'))


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
        if username in users and users[username] == password:
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

    cursor = db.cursor()
    cursor.execute("SELECT * FROM patients WHERE username = ?", (session['username'],))
    patients = cursor.fetchone()
    cursor.close()

    if request.method == "POST":
        age = int(request.form.get('age'))
        sex = request.form.get('sex') 
        address = request.form.get('address') 
        
        erythema = int(request.form.get('Erythema'))
        scaling = int(request.form.get('Scaling'))
        definite_borders = int(request.form.get('definite_borders'))
        itching = int(request.form.get('itching'))
        koebner_phenomenon = int(request.form.get('koebner_phenomenon'))
        polygonal_papules = int(request.form.get('polygonal_papules'))
        follicular_papules = int(request.form.get('follicular_papules'))
        oral_mucosal_involvement = int(request.form.get('oral_mucosal_involvement'))
        knee_and_elbow_involvement = int(request.form.get('knee_and_elbow_involvement'))
        scalp_involvement = int(request.form.get('scalp_involvement'))
        family_history = int(request.form.get('family_history'))
        melanin_incontinence = int(request.form.get('melanin_incontinence'))
        eosinophils_infiltrate = int(request.form.get('eosinophils_infiltrate'))
        PNL_infiltrate = int(request.form.get('PNL_infiltrate'))
        fibrosis_papillary_dermis = int(request.form.get('fibrosis_papillary_dermis'))
        exocytosis = int(request.form.get('exocytosis'))
        acanthosis = int(request.form.get('acanthosis'))
        hyperkeratosis = int(request.form.get('hyperkeratosis'))
        parakeratosis = int(request.form.get('parakeratosis'))
        clubbing_rete_ridges = int(request.form.get('clubbing_rete_ridges'))
        elongation_rete_ridges = int(request.form.get('elongation_rete_ridges'))
        thinning_suprapapillary_epidermis = int(request.form.get('thinning_suprapapillary_epidermis'))
        spongiform_pustule = int(request.form.get('spongiform_pustule'))
        munro_microabcess = int(request.form.get('munro_microabcess'))
        focal_hypergranulosis = int(request.form.get('focal_hypergranulosis'))
        disappearance_granular_layer = int(request.form.get('disappearance_granular_layer'))
        vacuolisation_damage_basal_layer = int(request.form.get('vacuolisation_damage_basal_layer'))
        spongiosis = int(request.form.get('spongiosis'))
        saw_tooth_appearance_retes = int(request.form.get('saw_tooth_appearance_retes'))
        follicular_horn_plug = int(request.form.get('follicular_horn_plug'))
        perifollicular_parakeratosis = int(request.form.get('perifollicular_parakeratosis'))
        inflammatory_mononuclear_infiltrate = int(request.form.get('inflammatory_mononuclear_infiltrate'))
        band_like_infiltrate = int(request.form.get('band_like_infiltrate'))
        
        features = [[erythema, scaling, definite_borders, itching, koebner_phenomenon, polygonal_papules, follicular_papules, oral_mucosal_involvement,
                     knee_and_elbow_involvement, scalp_involvement, family_history, melanin_incontinence, eosinophils_infiltrate, PNL_infiltrate,
                     fibrosis_papillary_dermis, exocytosis, acanthosis, hyperkeratosis, parakeratosis, clubbing_rete_ridges, elongation_rete_ridges,
                     thinning_suprapapillary_epidermis, spongiform_pustule, munro_microabcess, focal_hypergranulosis, disappearance_granular_layer,
                     vacuolisation_damage_basal_layer, spongiosis, saw_tooth_appearance_retes, follicular_horn_plug, perifollicular_parakeratosis,
                     inflammatory_mononuclear_infiltrate, band_like_infiltrate, age]]

        derma = model.predict(features)

        conditions = {
            0: "Psoriasis",
            1: "Seborrheic Dermatitis",
            2: "Lichen Planus",
            3: "Pityriasis Rosea",
            4: "Chronic Dermatitis",
            5: "Pityriasis Rubra Pilaris"
        }

        result = conditions.get(derma[0], "Unknown condition")
        
        cursor = db.cursor()
        cursor.execute(""" 
            INSERT INTO patients (username, name, age, sex, address, predicted_condition) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (session['username'], session['username'], age, sex, address, result))
        db.commit()

        return render_template('diagnosis.html', derma=result)

    return render_template('prediction.html')


if __name__ == '__main__':
    app.run(debug=True)
