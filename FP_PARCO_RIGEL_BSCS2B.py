# My Project: Skin Disease Detection

from flask import Flask, render_template, request
import pickle

##FILE PATH OF TEMPLATE FOLDER
app = Flask(__name__, template_folder='template')

fileObj = open('model2.obj', 'rb')
model = pickle.load(fileObj)

@app.route("/")
def index():
    return render_template('app2.html')

@app.route("/predict", methods=['POST', 'GET'])
def predict(derma=None):
    if request.method == "POST":
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
        age = int(request.form.get('age'))

        derma = model.predict([[erythema,scaling,definite_borders,itching,koebner_phenomenon,polygonal_papules,follicular_papules,oral_mucosal_involvement,
                                knee_and_elbow_involvement,scalp_involvement,family_history,
                                melanin_incontinence,eosinophils_infiltrate,PNL_infiltrate,fibrosis_papillary_dermis,
                                exocytosis,acanthosis,hyperkeratosis,parakeratosis,clubbing_rete_ridges,elongation_rete_ridges,
                                thinning_suprapapillary_epidermis,spongiform_pustule,munro_microabcess,focal_hypergranulosis,
                                disappearance_granular_layer,vacuolisation_damage_basal_layer,spongiosis,saw_tooth_appearance_retes,
                                follicular_horn_plug,perifollicular_parakeratosis,inflammatory_mononuclear_infiltrate,band_like_infiltrate,age]])

        if derma == 0:
            derma = "psoriasis"
        elif derma == 1:
            derma = "Seboreic dermatitis"
        elif derma == 2:
            derma = "lichen planus"
        elif derma == 3:
            derma = "Pityriasis rosea"
        elif derma == 4:
            derma = "chronic dermatitis"
        elif derma == 5:
            derma = "Pityriasis rubra Pilaris"
        else:
            return render_template('app2.html')
        return render_template('app2.html', derma=derma)
    return render_template('app2.html')

if __name__ == "__main__":
    app.run(debug=True)