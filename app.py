import os
import pickle
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)
app.secret_key = "pokemon-ml-exit-exam-secret-key"

# Path to the trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "random_forest_model.pkl")

# Load model and preprocessor safely
model_data = None
model = None
preprocessor = None

try:
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            model_data = pickle.load(f)
            model = model_data.get("model")
            preprocessor = model_data.get("preprocessor")
            print("Successfully loaded random_forest_model.pkl!")
            print(f"Model classes: {getattr(model, 'classes_', 'N/A')}")
    else:
        print(f"Warning: Model file not found at {MODEL_PATH}")
except Exception as e:
    print(f"Error loading model: {e}")

# Pokemon Elemental Types Knowledge Base & Archetype Profiles
POKEMON_TYPES = {
    'dragon': {
        'name': 'Dragon', 'color': '#6F35FC', 'bg': 'linear-gradient(135deg, #6F35FC, #4924A1)', 'icon': '🐉',
        'hp': 83, 'attack': 105, 'defense': 86, 'height_dm': 20, 'weight_hg': 1160, 'base_experience': 213,
        'desc': 'Legendary draconic constitution. Boasts colossal base stats, dominant attack power, and elite battle presence.'
    },
    'steel': {
        'name': 'Steel', 'color': '#B7B7CE', 'bg': 'linear-gradient(135deg, #B7B7CE, #787887)', 'icon': '⚙️',
        'hp': 65, 'attack': 92, 'defense': 126, 'height_dm': 18, 'weight_hg': 1800, 'base_experience': 195,
        'desc': 'Impenetrable metallic alloy. Unmatched physical defense, tremendous body mass, and exceptional durability.'
    },
    'rock': {
        'name': 'Rock', 'color': '#B6A136', 'bg': 'linear-gradient(135deg, #B6A136, #786B24)', 'icon': '🪨',
        'hp': 67, 'attack': 89, 'defense': 108, 'height_dm': 13, 'weight_hg': 920, 'base_experience': 156,
        'desc': 'Ancient mineral fortitude. Formidable physical defense, high weight density, and rugged durability.'
    },
    'fighting': {
        'name': 'Fighting', 'color': '#C22E28', 'bg': 'linear-gradient(135deg, #C22E28, #7F1E1B)', 'icon': '🥊',
        'hp': 75, 'attack': 102, 'defense': 73, 'height_dm': 13, 'weight_hg': 650, 'base_experience': 180,
        'desc': 'Peak martial athleticism. Explosive physical attack, muscular conditioning, and relentless close-range pressure.'
    },
    'fire': {
        'name': 'Fire', 'color': '#EE8130', 'bg': 'linear-gradient(135deg, #EE8130, #9C531F)', 'icon': '🔥',
        'hp': 69, 'attack': 85, 'defense': 68, 'height_dm': 12, 'weight_hg': 600, 'base_experience': 169,
        'desc': 'Intense thermal combustion. High offensive damage output, fiery battle velocity, and devastating attacks.'
    },
    'water': {
        'name': 'Water', 'color': '#6390F0', 'bg': 'linear-gradient(135deg, #6390F0, #3860B8)', 'icon': '💧',
        'hp': 72, 'attack': 74, 'defense': 73, 'height_dm': 13, 'weight_hg': 530, 'base_experience': 155,
        'desc': 'Adaptable oceanic resilience. Excellent HP stamina, versatile defensive balance, and flowing battle flexibility.'
    },
    'grass': {
        'name': 'Grass', 'color': '#7AC74C', 'bg': 'linear-gradient(135deg, #7AC74C, #4E8234)', 'icon': '🌿',
        'hp': 67, 'attack': 73, 'defense': 71, 'height_dm': 11, 'weight_hg': 330, 'base_experience': 155,
        'desc': 'Symbiotic botanical endurance. Balanced health and defense stats, natural vitality, and steady battlefield recovery.'
    },
    'electric': {
        'name': 'Electric', 'color': '#F7D02C', 'bg': 'linear-gradient(135deg, #F7D02C, #A1871B)', 'icon': '⚡',
        'hp': 63, 'attack': 72, 'defense': 66, 'height_dm': 9, 'weight_hg': 380, 'base_experience': 164,
        'desc': 'High-frequency ionization. Rapid speed, lightweight agile physiology, and sudden discharge potential.'
    },
    'psychic': {
        'name': 'Psychic', 'color': '#F95587', 'bg': 'linear-gradient(135deg, #F95587, #A13556)', 'icon': '🔮',
        'hp': 71, 'attack': 72, 'defense': 68, 'height_dm': 12, 'weight_hg': 550, 'base_experience': 190,
        'desc': 'Transcendental telepathic mastery. Tremendous mental discipline, high base experience, and reality-bending power.'
    },
    'ground': {
        'name': 'Ground', 'color': '#E2BF65', 'bg': 'linear-gradient(135deg, #E2BF65, #927D44)', 'icon': '🏜️',
        'hp': 73, 'attack': 95, 'defense': 84, 'height_dm': 13, 'weight_hg': 850, 'base_experience': 155,
        'desc': 'Tectonic earth power. Sturdy grounded posture, bone-crushing attack impact, and solid physical armor.'
    },
    'ghost': {
        'name': 'Ghost', 'color': '#735797', 'bg': 'linear-gradient(135deg, #735797, #493963)', 'icon': '👻',
        'hp': 63, 'attack': 74, 'defense': 80, 'height_dm': 12, 'weight_hg': 320, 'base_experience': 158,
        'desc': 'Spectral incorporeal presence. Low physical weight, evasive supernatural traits, and deceptive combat endurance.'
    },
    'poison': {
        'name': 'Poison', 'color': '#A33EA1', 'bg': 'linear-gradient(135deg, #A33EA1, #682768)', 'icon': '☠️',
        'hp': 68, 'attack': 75, 'defense': 70, 'height_dm': 12, 'weight_hg': 370, 'base_experience': 157,
        'desc': 'Biochemical venom synthesis. Resilient bodily defenses, gradual wear-down capability, and toxic battlefield control.'
    },
    'dark': {
        'name': 'Dark', 'color': '#705746', 'bg': 'linear-gradient(135deg, #705746, #49392E)', 'icon': '🌑',
        'hp': 72, 'attack': 90, 'defense': 70, 'height_dm': 12, 'weight_hg': 510, 'base_experience': 166,
        'desc': 'Shadow-veiled tactical strikes. Sharp offensive impact, deceptive maneuvers, and high critical threat level.'
    },
    'fairy': {
        'name': 'Fairy', 'color': '#D685AD', 'bg': 'linear-gradient(135deg, #D685AD, #924B70)', 'icon': '✨',
        'hp': 70, 'attack': 65, 'defense': 72, 'height_dm': 10, 'weight_hg': 350, 'base_experience': 164,
        'desc': 'Mystical lunar radiance. Protective aura shielding against draconic energy, charming presence, and magical resilience.'
    },
    'bug': {
        'name': 'Bug', 'color': '#A6B91A', 'bg': 'linear-gradient(135deg, #A6B91A, #6D7815)', 'icon': '🐛',
        'hp': 58, 'attack': 68, 'defense': 71, 'height_dm': 8, 'weight_hg': 240, 'base_experience': 140,
        'desc': 'Chitinous exoskeleton tenacity. Rapid growth rate, compact nimble build, and surprising survival tenacity.'
    },
    'normal': {
        'name': 'Normal', 'color': '#A8A878', 'bg': 'linear-gradient(135deg, #A8A878, #6D6D4E)', 'icon': '⭐',
        'hp': 77, 'attack': 74, 'defense': 61, 'height_dm': 11, 'weight_hg': 580, 'base_experience': 150,
        'desc': 'Universal physiological versatility. Generous stamina pool, varied move affinities, and dependable consistency.'
    },
    'ice': {
        'name': 'Ice', 'color': '#96D9D6', 'bg': 'linear-gradient(135deg, #96D9D6, #638D8D)', 'icon': '❄️',
        'hp': 73, 'attack': 85, 'defense': 73, 'height_dm': 13, 'weight_hg': 650, 'base_experience': 165,
        'desc': 'Glacial cryo-crystallization. High piercing offensive threat, chilling attacks, and sub-zero adaptation.'
    },
    'flying': {
        'name': 'Flying', 'color': '#A98FF3', 'bg': 'linear-gradient(135deg, #A98FF3, #6D5E9C)', 'icon': '🪶',
        'hp': 71, 'attack': 78, 'defense': 68, 'height_dm': 12, 'weight_hg': 350, 'base_experience': 183,
        'desc': 'Aerodynamic thermal soaring. Swift air currents, lightweight body construction, and sweeping sky dominance.'
    }
}

# Average Pokemon benchmarks for comparison
DATASET_BENCHMARKS = {
    'hp': {'mean': 69.2, 'min': 1, 'max': 255},
    'attack': {'mean': 78.3, 'min': 5, 'max': 190},
    'defense': {'mean': 73.8, 'min': 5, 'max': 230},
    'height_dm': {'mean': 12.2, 'min': 1, 'max': 200},
    'weight_hg': {'mean': 680.5, 'min': 1, 'max': 9999},
    'base_experience': {'mean': 154.2, 'min': 36, 'max': 608}
}

def estimate_pokemon_type(hp, attack, defense, height_dm, weight_hg, base_experience):
    """Calculates elemental type affinity score based on Pokemon stat profile."""
    scores = {}
    weights = {'hp': 1.1, 'attack': 1.6, 'defense': 1.3, 'height_dm': 0.8, 'weight_hg': 0.8, 'base_experience': 1.5}
    scales = {'hp': 25, 'attack': 25, 'defense': 25, 'height_dm': 7, 'weight_hg': 450, 'base_experience': 45}

    input_vals = {
        'hp': hp,
        'attack': attack,
        'defense': defense,
        'height_dm': height_dm,
        'weight_hg': weight_hg,
        'base_experience': base_experience
    }

    for t_key, t_info in POKEMON_TYPES.items():
        diff_sq = 0.0
        for feat in ['hp', 'attack', 'defense', 'height_dm', 'weight_hg', 'base_experience']:
            diff = (input_vals[feat] - t_info[feat]) / scales[feat]
            diff_sq += weights[feat] * (diff ** 2)
        sim = 1.0 / (1.0 + diff_sq)
        scores[t_key] = sim

    sorted_types = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best_key, best_score = sorted_types[0]
    second_key = sorted_types[1][0] if len(sorted_types) > 1 else None
    
    # Calculate relative confidence
    top_sum = sum(s for _, s in sorted_types[:4])
    confidence = round((best_score / top_sum) * 100, 1) if top_sum > 0 else 55.0

    return POKEMON_TYPES[best_key], confidence, POKEMON_TYPES[second_key] if second_key else None

def determine_archetype(hp, attack, defense, height_dm, weight_hg, base_exp):
    """Classifies combat playstyle archetype."""
    if defense >= 100 and hp >= 80:
        return {
            'role': 'Sturdy Tank / Fortress',
            'desc': 'Extremely high bulk and defensive endurance. Capable of absorbing devastating hits and anchoring the team.'
        }
    elif attack >= 100 and base_exp >= 180:
        return {
            'role': 'Heavy Physical Sweeper',
            'desc': 'Massive attack power with high battle readiness. Specializes in rapid offensive breakthroughs and team sweeps.'
        }
    elif attack >= 90 and defense >= 80:
        return {
            'role': 'Balanced Bruiser',
            'desc': 'Well-rounded physical offensive and defensive balance. A versatile front-line combatant in any arena.'
        }
    elif weight_hg < 300 and height_dm < 10:
        return {
            'role': 'Agile Scout / Fast Striker',
            'desc': 'Lightweight and compact anatomy optimized for rapid flanking, evasion, and momentum-building strikes.'
        }
    else:
        return {
            'role': 'Versatile All-Rounder',
            'desc': 'Dependable distribution across health, defensive durability, and battle experience.'
        }

@app.route("/")
def index():
    """Home Page: Project Overview, Dataset Insights, and ML Model Benchmarks."""
    overview_data = {
        "dataset_rows": 1351,
        "dataset_features": 10,
        "best_model_name": "Tuned Random Forest Classifier",
        "best_accuracy": "68.63%",
        "best_f1_score": "0.6806",
        "best_precision": "0.6817",
        "best_recall": "0.6825",
        "cv_score": "0.6570",
        "model_comparison": [
            {"model": "Random Forest", "mean_f1": "0.6385", "std": "0.0383", "badge": "Winner", "rank": 1},
            {"model": "Logistic Regression", "mean_f1": "0.6045", "std": "0.0294", "badge": "2nd", "rank": 2},
            {"model": "Decision Tree", "mean_f1": "0.5872", "std": "0.0140", "badge": "3rd", "rank": 3},
            {"model": "KNN (K-Nearest Neighbors)", "mean_f1": "0.5545", "std": "0.0289", "badge": "4th", "rank": 4},
            {"model": "SVM (Support Vector Machine)", "mean_f1": "0.4901", "std": "0.0169", "badge": "5th", "rank": 5}
        ],
        "hyperparameters": {
            "n_estimators": 200,
            "max_depth": 20,
            "min_samples_split": 5,
            "min_samples_leaf": 2,
            "max_features": "sqrt",
            "class_weight": "balanced"
        }
    }
    return render_template("index.html", data=overview_data)

@app.route("/predict", methods=["GET", "POST"])
def predict():
    """Prediction Page: Input form for HP, Attack, Defense, Height, Weight, Base Exp."""
    if request.method == "POST":
        try:
            hp = float(request.form.get("hp", 65))
            attack = float(request.form.get("attack", 75))
            defense = float(request.form.get("defense", request.form.get("defence", 70)))
            height_dm = float(request.form.get("height", 10))
            weight_hg = float(request.form.get("weight", 500))
            base_exp = float(request.form.get("base_experience", 140))
            type_1 = request.form.get("type_1", "").strip().lower()
            type_2 = request.form.get("type_2", "").strip().lower()

            # If user didn't select type_1 or left it auto
            if not type_1 or type_1 == "auto":
                est_type, _, _ = estimate_pokemon_type(hp, attack, defense, height_dm, weight_hg, base_exp)
                type_1 = est_type['name'].lower()

            if not type_2 or type_2 == "none" or type_2 == "auto":
                type_2 = "No secondary type"

            # Create input DataFrame for the trained preprocessor
            input_df = pd.DataFrame([{
                'height_dm': height_dm,
                'weight_hg': weight_hg,
                'base_experience': base_exp,
                'hp': hp,
                'defense': defense,
                'type_1': type_1,
                'type_2': type_2
            }])

            # Run prediction through the pickle model
            predicted_class = "Medium"
            probabilities = {"High": 33.3, "Medium": 33.4, "Low": 33.3}

            if model and preprocessor:
                X_trans = preprocessor.transform(input_df)
                raw_pred = model.predict(X_trans)[0]
                predicted_class = str(raw_pred)
                
                if hasattr(model, "predict_proba"):
                    probs = model.predict_proba(X_trans)[0]
                    for cls_name, prob in zip(model.classes_, probs):
                        probabilities[str(cls_name)] = round(float(prob) * 100, 1)

            # Estimate Pokemon Elemental Type & Archetype
            pred_type_info, type_confidence, secondary_type_info = estimate_pokemon_type(
                hp, attack, defense, height_dm, weight_hg, base_exp
            )
            archetype_info = determine_archetype(hp, attack, defense, height_dm, weight_hg, base_exp)

            # Benchmark comparisons (percentages against average)
            stat_comparisons = {
                'hp': {'val': hp, 'pct': min(100, round((hp / DATASET_BENCHMARKS['hp']['mean']) * 50)), 'mean': DATASET_BENCHMARKS['hp']['mean']},
                'attack': {'val': attack, 'pct': min(100, round((attack / DATASET_BENCHMARKS['attack']['mean']) * 50)), 'mean': DATASET_BENCHMARKS['attack']['mean']},
                'defense': {'val': defense, 'pct': min(100, round((defense / DATASET_BENCHMARKS['defense']['mean']) * 50)), 'mean': DATASET_BENCHMARKS['defense']['mean']},
                'height_dm': {'val': height_dm, 'pct': min(100, round((height_dm / DATASET_BENCHMARKS['height_dm']['mean']) * 50)), 'mean': DATASET_BENCHMARKS['height_dm']['mean']},
                'weight_hg': {'val': weight_hg, 'pct': min(100, round((weight_hg / DATASET_BENCHMARKS['weight_hg']['mean']) * 50)), 'mean': DATASET_BENCHMARKS['weight_hg']['mean']},
                'base_experience': {'val': base_exp, 'pct': min(100, round((base_exp / DATASET_BENCHMARKS['base_experience']['mean']) * 50)), 'mean': DATASET_BENCHMARKS['base_experience']['mean']}
            }

            result_payload = {
                "inputs": {
                    "hp": hp,
                    "attack": attack,
                    "defense": defense,
                    "height": height_dm,
                    "weight": weight_hg,
                    "base_experience": base_exp,
                    "type_1": type_1.title(),
                    "type_2": type_2.title() if type_2 != "No secondary type" else "None"
                },
                "attack_class": predicted_class,
                "probabilities": probabilities,
                "confidence": probabilities.get(predicted_class, 50.0),
                "predicted_type": pred_type_info,
                "type_confidence": type_confidence,
                "secondary_type": secondary_type_info,
                "archetype": archetype_info,
                "stat_comparisons": stat_comparisons
            }

            return render_template("result.html", result=result_payload)

        except Exception as e:
            return render_template("predict.html", error=f"Prediction Error: {str(e)}", all_types=POKEMON_TYPES)

    return render_template("predict.html", all_types=POKEMON_TYPES)

@app.route("/api/predict", methods=["POST"])
def api_predict():
    """JSON REST API endpoint for predictions."""
    try:
        data = request.get_json(force=True)
        hp = float(data.get("hp", 65))
        attack = float(data.get("attack", 75))
        defense = float(data.get("defense", data.get("defence", 70)))
        height_dm = float(data.get("height", 10))
        weight_hg = float(data.get("weight", 500))
        base_exp = float(data.get("base_experience", 140))
        type_1 = data.get("type_1", "unknown").lower()
        type_2 = data.get("type_2", "No secondary type")

        input_df = pd.DataFrame([{
            'height_dm': height_dm,
            'weight_hg': weight_hg,
            'base_experience': base_exp,
            'hp': hp,
            'defense': defense,
            'type_1': type_1,
            'type_2': type_2
        }])

        predicted_class = "Medium"
        probabilities = {}
        if model and preprocessor:
            X_trans = preprocessor.transform(input_df)
            predicted_class = str(model.predict(X_trans)[0])
            if hasattr(model, "predict_proba"):
                probs = model.predict_proba(X_trans)[0]
                for cls_name, prob in zip(model.classes_, probs):
                    probabilities[str(cls_name)] = round(float(prob) * 100, 2)

        pred_type, type_conf, sec_type = estimate_pokemon_type(hp, attack, defense, height_dm, weight_hg, base_exp)

        return jsonify({
            "status": "success",
            "predicted_attack_class": predicted_class,
            "probabilities": probabilities,
            "predicted_pokemon_type": pred_type['name'],
            "type_confidence": type_conf,
            "secondary_affinity": sec_type['name'] if sec_type else None
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
