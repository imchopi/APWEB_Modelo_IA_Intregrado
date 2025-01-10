import streamlit as st
import pandas as pd
import joblib
import json

# Configuración de la página
st.set_page_config(
    page_title="Predicción de Personalidad",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilo CSS personalizado
st.markdown("""
    <style>
        .main {
            padding: 2rem;
        }
        .stProgress > div > div > div > div {
            background-color: #1f77b4;
        }
        .category-title {
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
        }
        .question-container {
            background-color: white;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .small-text {
            font-size: 0.8rem;
            color: #666;
        }
    </style>
""", unsafe_allow_html=True)

# Título y descripción inicial
st.title("🎯 Predicción de Personalidad")
st.image("img/personality.png", use_container_width=True)

# Creación de dos columnas principales
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Complete el test de personalidad")
    st.markdown("""
        <div style='background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem;'>
            ⏱️ Cada test tarda una media de 10-15 mins en ser completado
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.image("img/BarChartScene.png", use_container_width=True)
    st.markdown("""
        <p style='text-align: center; color: #666;'>
            📊 Los 10 principales países según el número de entrevistas
        </p>
    """, unsafe_allow_html=True)

# Cargar modelo y mapeo
@st.cache_resource
def load_model():
    model = joblib.load("data/model/personality_model.joblib")
    with open("data/model/category_mapping.json", "r") as f:
        category_mapping = json.load(f)
    return model, category_mapping

model, category_mapping = load_model()

# Diccionario completo de preguntas
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

# Categorías
categories = {
    "Extroversión": ["EXT1", "EXT2", "EXT3", "EXT4", "EXT5", "EXT6", "EXT7", "EXT8", "EXT9", "EXT10"],
    "Inestabilidad emocional": ["EST1", "EST2", "EST3", "EST4", "EST5", "EST6", "EST7", "EST8", "EST9", "EST10"],
    "Amabilidad": ["AGR1", "AGR2", "AGR3", "AGR4", "AGR5", "AGR6", "AGR7", "AGR8", "AGR9", "AGR10"],
    "Responsabilidad": ["CSN1", "CSN2", "CSN3", "CSN4", "CSN5", "CSN6", "CSN7", "CSN8", "CSN9", "CSN10"],
    "Apertura a la experiencia": ["OPN1", "OPN2", "OPN3", "OPN4", "OPN5", "OPN6", "OPN7", "OPN8", "OPN9", "OPN10"]
}

# Colores para categorías
category_colors = {
    "Extroversión": "#1f77b4",
    "Inestabilidad emocional": "#ff7f0e",
    "Amabilidad": "#2ca02c",
    "Responsabilidad": "#d62728",
    "Apertura a la experiencia": "#9467bd"
}

# Inicializar estado de la sesión

# if 'responses' not in st.session_state:
    # st.session_state.responses = {}

if 'responses' not in st.session_state:
    st.session_state.responses = {q_key: "Neutral" for q_key in questions.keys()}

# Barra de progreso
total_questions = sum(len(qs) for qs in categories.values())
# completed_questions = len([r for r in st.session_state.responses.values() if r != "Seleccione una opción"])
completed_questions = len([r for r in st.session_state.responses.values() if r != "Neutral"])  # Solo respuestas distintas de "Neutral"
progress = completed_questions / total_questions

st.progress(progress)
st.markdown(f"""
    <div style='text-align: center; color: #666;'>
        Progreso: {completed_questions}/{total_questions} preguntas respondidas ({int(progress * 100)}%)
    </div>
""", unsafe_allow_html=True) 



# Crear tabs para las categorías
tabs = st.tabs(list(categories.keys()))

for idx, (category, q_keys) in enumerate(categories.items()):
    with tabs[idx]:
        st.markdown(f"""
            <div class='category-title' style='background-color: {category_colors[category]}20;'>
                <h2 style='color: {category_colors[category]};'>{category}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        for q_key in q_keys:
            st.markdown(f"""
                <div class='question-container'>
                    {questions[q_key]}
                </div>
            """, unsafe_allow_html=True)
            
            response = st.select_slider(
                "",
                options=["Totalmente en desacuerdo", "En desacuerdo", "Neutral", "De acuerdo", "Totalmente de acuerdo"],
                key=q_key,
                value="Neutral"
            )
            st.session_state.responses[q_key] = response




# Botón de predicción
if st.button("📊 Realizar predicción", type="primary", use_container_width=True):
    if len(st.session_state.responses) == total_questions:
        with st.spinner('Analizando respuestas...'):
            response_mapping = {
                "Totalmente en desacuerdo": 1,
                "En desacuerdo": 2,
                "Neutral": 3,
                "De acuerdo": 4,
                "Totalmente de acuerdo": 5
            }
            
            data = [response_mapping[resp] for resp in st.session_state.responses.values()]
            
            try:
                prediction = model.predict([data])
                result = category_mapping[str(prediction[0])]
                
                st.markdown("""
                    <div style='background-color: #f0f2f6; padding: 2rem; border-radius: 0.5rem; margin: 2rem 0;'>
                        <h2 style='color: #1f77b4; text-align: center;'>🎉 Resultados del Análisis</h2>
                """, unsafe_allow_html=True)
                
                st.success(f"Su tipo de personalidad es: {result}")
                
                results_df = pd.DataFrame({
                    'Categoría': list(categories.keys()),
                    'Puntuación': [sum(data[i:i+10])/10 for i in range(0, len(data), 10)]
                })
                
                st.bar_chart(results_df.set_index('Categoría'))
                
                st.download_button(
                    label="📥 Descargar resultados",
                    data=results_df.to_csv(index=False),
                    file_name="resultados_personalidad.csv",
                    mime="text/csv"
                )
                
                st.markdown("</div>", unsafe_allow_html=True)
                st.balloons()
                
            except Exception as e:
                st.error(f"Error en la predicción: {e}")
    else:
        st.warning("Por favor, responda todas las preguntas antes de continuar.")

# Pie de página
st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0; border-top: 1px solid #eee; margin-top: 2rem;'>
        <p>Desarrollado con ❤️ por:</br>Adrian Perogil</br>Hugo Peralta</br>Natalie Pilkington</p>
        <p class='small-text'>Versión 1.1.0</p>
    </div>
""", unsafe_allow_html=True)