# app.py (entrenamiento + servidor)
import pandas as pd
import pickle
from flask import Flask, render_template, request
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Datos simulados
data = {
    "edad": [25, 30, 45, 35, 50, 28, 60],
    "sexo": ["M", "F", "F", "M", "F", "M", "F"],
    "peso": [70, 60, 80, 90, 65, 75, 85],
    "altura": [170, 160, 165, 180, 155, 175, 160],
    "actividad": ["alta", "moderada", "baja", "alta", "baja", "moderada", "baja"],
    "objetivo": ["mantener", "bajar", "bajar", "subir", "bajar", "mantener", "subir"],
    "condicion": ["ninguna", "diabetes", "hipertension", "ninguna", "diabetes", "ninguna", "hipertension"],
    "plan": ["Plan A", "Plan B", "Plan C", "Plan A", "Plan B", "Plan A", "Plan C"]
}
df = pd.DataFrame(data)

# Codificación
label_encoders = {}
for col in ["sexo", "actividad", "objetivo", "condicion", "plan"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

X = df.drop(columns=["plan"])
y = df["plan"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_scaled, y)

# Guardar modelo y herramientas
with open("modelo.pkl", "wb") as f: pickle.dump(model, f)
with open("scaler.pkl", "wb") as f: pickle.dump(scaler, f)
with open("label_encoders.pkl", "wb") as f: pickle.dump(label_encoders, f)

# App Flask
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    plan = None
    if request.method == 'POST':
        edad = int(request.form['edad'])
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        sexo = request.form['sexo']
        actividad = request.form['actividad']
        objetivo = request.form['objetivo']
        condicion = request.form['condicion']

        with open("modelo.pkl", "rb") as f: model = pickle.load(f)
        with open("scaler.pkl", "rb") as f: scaler = pickle.load(f)
        with open("label_encoders.pkl", "rb") as f: label_encoders = pickle.load(f)

        entrada = pd.DataFrame([{
            "edad": edad,
            "sexo": label_encoders["sexo"].transform([sexo])[0],
            "peso": peso,
            "altura": altura,
            "actividad": label_encoders["actividad"].transform([actividad])[0],
            "objetivo": label_encoders["objetivo"].transform([objetivo])[0],
            "condicion": label_encoders["condicion"].transform([condicion])[0],
        }])

        entrada_scaled = scaler.transform(entrada)
        pred = model.predict(entrada_scaled)
        plan = label_encoders["plan"].inverse_transform(pred)[0]

    return render_template("index.html", plan=plan)

if __name__ == "__main__":
    app.run(debug=True)
