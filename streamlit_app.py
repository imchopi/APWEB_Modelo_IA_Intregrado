import streamlit as st
import joblib
import pandas as pd
import json

st.title("Predicción de Personalidad")
st.write("Responda las siguientes preguntas para predecir su personalidad.")
st.image("img/personality.png", use_container_width=True)

# Carga el modelo entrenado y las asignaciones
model = joblib.load("model/personality_model.joblib")
with open("model/category_mapping.json", "r") as f:
    category_mapping = json.load(f)

# Preguntas de personalidad
questions = {
    "EXT1": "Soy el alma de la fiesta.",
    "EXT2": "No hablo mucho.",
    "EXT3": "Me siento cómodo alrededor de la gente.",
    "EXT4": "Me mantengo en segundo plano.",
    "EXT5": "Empiezo conversaciones.",
    "EXT6": "Tengo poco que decir.",
    "EXT7": "Hablo con muchas personas diferentes en las fiestas.",
    "EXT8": "No me gusta llamar la atención.",
    "EXT9": "No me importa ser el centro de atención.",
    "EXT10": "Soy callado alrededor de extraños.",
    "EST1": "Me estreso fácilmente.",
    "EST2": "Estoy relajado la mayor parte del tiempo.",
    "EST3": "Me preocupo por las cosas.",
    "EST4": "Rara vez me siento triste.",
    "EST5": "Me perturbo fácilmente.",
    "EST6": "Me molesto fácilmente.",
    "EST7": "Cambio de humor a menudo.",
    "EST8": "Tengo cambios de humor frecuentes.",
    "EST9": "Me irrito fácilmente.",
    "EST10": "A menudo me siento triste.",
    "AGR1": "Siento poco interés por los demás.",
    "AGR2": "Estoy interesado en la gente.",
    "AGR3": "Insulto a las personas.",
    "AGR4": "Simpatizo con los sentimientos de los demás.",
    "AGR5": "No estoy interesado en los problemas de los demás.",
    "AGR6": "Tengo un corazón blando.",
    "AGR7": "No estoy realmente interesado en los demás.",
    "AGR8": "Dedico tiempo a los demás.",
    "AGR9": "Siento las emociones de los demás.",
    "AGR10": "Hago que la gente se sienta a gusto.",
    "CSN1": "Siempre estoy preparado.",
    "CSN2": "Dejo mis pertenencias por ahí.",
    "CSN3": "Presto atención a los detalles.",
    "CSN4": "Hago un lío de las cosas.",
    "CSN5": "Hago las tareas de inmediato.",
    "CSN6": "A menudo olvido poner las cosas en su lugar.",
    "CSN7": "Me gusta el orden.",
    "CSN8": "Evito mis responsabilidades.",
    "CSN9": "Sigo un horario.",
    "CSN10": "Soy exigente en mi trabajo.",
    "OPN1": "Tengo un vocabulario rico.",
    "OPN2": "Tengo dificultad para entender ideas abstractas.",
    "OPN3": "Tengo una imaginación vívida.",
    "OPN4": "No estoy interesado en ideas abstractas.",
    "OPN5": "Tengo excelentes ideas.",
    "OPN6": "No tengo una buena imaginación.",
    "OPN7": "Soy rápido para entender las cosas.",
    "OPN8": "Uso palabras difíciles.",
    "OPN9": "Dedico tiempo a reflexionar sobre las cosas.",
    "OPN10": "Estoy lleno de ideas."
}

# Mapeo de respuestas a valores numéricos
response_mapping = {
    "En desacuerdo": 1,
    "Ligeramente en desacuerdo": 2,
    "Neutro": 3,
    "Ligeramente de acuerdo": 4,
    "De acuerdo": 5
}

responses = {}
for key, question in questions.items():
    responses[key] = st.radio(
        question, 
        ["En desacuerdo", "Ligeramente en desacuerdo", "Neutro", "Ligeramente de acuerdo", "De acuerdo"]
    )

# Prepara los datos para la predicción
input_data = [response_mapping[responses[key]] for key in questions.keys()]
input_df = pd.DataFrame([input_data], columns=questions.keys())

# Realiza la predicción
if st.button("Predecir personalidad"):
    prediction = model.predict(input_df)[0]
    st.success(f"Su personalidad se clasifica como: {category_mapping[prediction]}", icon="✅")