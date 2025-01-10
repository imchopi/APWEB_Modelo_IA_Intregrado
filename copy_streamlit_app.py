import streamlit as st
import joblib
import pandas as pd
import json

st.title("Predicción de Personalidad")
st.image("img/personality.png", use_container_width=True)
st.markdown("<h3>Seleccione una opción dentro de cada categoría para predecir su personalidad.</h2>", unsafe_allow_html=True)


# Carga el modelo entrenado y las asignaciones
model = joblib.load("data/model/personality_model.joblib")
with open("data/model/category_mapping.json", "r") as f:
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

# Agrupar preguntas por categorías
categories = {
    "Extroversión": ["EXT1", "EXT2", "EXT3", "EXT4", "EXT5", "EXT6", "EXT7", "EXT8", "EXT9", "EXT10"],
    "Inestabilidad emocional": ["EST1", "EST2", "EST3", "EST4", "EST5", "EST6", "EST7", "EST8", "EST9", "EST10"],
    "Amabilidad": ["AGR1", "AGR2", "AGR3", "AGR4", "AGR5", "AGR6", "AGR7", "AGR8", "AGR9", "AGR10"],
    "Responsabilidad": ["CSN1", "CSN2", "CSN3", "CSN4", "CSN5", "CSN6", "CSN7", "CSN8", "CSN9", "CSN10"],
    "Apertura a la experiencia": ["OPN1", "OPN2", "OPN3", "OPN4", "OPN5", "OPN6", "OPN7", "OPN8", "OPN9", "OPN10"]
}

# Recopilar respuestas
responses = []

# Definir colores para cada epígrafe
category_colors = {
    "Extroversión": "blue",
    "Inestabilidad emocional": "red",
    "Amabilidad": "green",
    "Responsabilidad": "purple",
    "Apertura a la experiencia": "orange"
}


for category, q_keys in categories.items():
    # st.header(category)
    st.markdown(f"<h2 style='color: {category_colors[category]};'>{category}</h2>", unsafe_allow_html=True)
    for q_key in q_keys:
        st.markdown(f"<h4>{questions[q_key]}</h4>", unsafe_allow_html=True)
        response = st.radio("", ["Seleccione una opción", "Totalmente en desacuerdo", "En desacuerdo", "Neutral", "De acuerdo", "Totalmente de acuerdo"], index=0, key=q_key)
        responses.append(response)

# Convertir respuestas a un formato adecuado para el modelo
response_mapping = {
    "Totalmente en desacuerdo": 1,
    "En desacuerdo": 2,
    "Neutral": 3,
    "De acuerdo": 4,
    "Totalmente de acuerdo": 5
}
data = [response_mapping[response] for response in responses if response != "Seleccione una opción"]

if st.button("Predecir"):
    if len(data) == len(questions):
        try:
            prediction = model.predict([data])
            result = category_mapping[str(prediction[0])]
            st.success(f"Su personalidad se clasifica como: {result}", icon="✅")
            st.balloons()
        except KeyError as e:
            st.error(f"Error: Predicción desconocida {e}", icon="❌")
        except Exception as e:
            st.error(f"Error: {e}", icon="❌")
    else:
        st.error("Por favor, responda todas las preguntas antes de predecir.", icon="❌")