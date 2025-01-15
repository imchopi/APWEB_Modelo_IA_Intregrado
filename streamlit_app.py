import streamlit as st
import pandas as pd
import joblib
import json

# Configuración de la página
st.set_page_config(
    page_title="Predicción de Personalidad",
    # layout="wide",
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
            font-weight: bold;
        }
        .small-text {
            font-size: 0.8rem;
            color: #666;
        }
        .stButton>button {            
            margin-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Título y descripción inicial
st.title("🎯 Predicción de Personalidad")
st.image("img/personality.png", use_container_width=True)

# Descripción del test
st.markdown("### 📝 Complete el test de personalidad")
st.markdown("""
    <div style="background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem;">
        ⏱️ Cada test tarda una media de 10-15 mins en ser completado
    </div>
""", unsafe_allow_html=True)

# Imagen de países alineada a la izquierda
st.image("img/BarChartScene_white.png", use_container_width=True)
st.markdown("""
    <p style="text-align: left; color: #666;">
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

# Diccionario de preguntas
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
    "Extraversión": ["EXT1", "EXT2", "EXT3", "EXT4", "EXT5", "EXT6", "EXT7", "EXT8", "EXT9", "EXT10"],
    "Inestabilidad emocional": ["EST1", "EST2", "EST3", "EST4", "EST5", "EST6", "EST7", "EST8", "EST9", "EST10"],
    "Amabilidad": ["AGR1", "AGR2", "AGR3", "AGR4", "AGR5", "AGR6", "AGR7", "AGR8", "AGR9", "AGR10"],
    "Responsabilidad": ["CSN1", "CSN2", "CSN3", "CSN4", "CSN5", "CSN6", "CSN7", "CSN8", "CSN9", "CSN10"],
    "Apertura a la experiencia": ["OPN1", "OPN2", "OPN3", "OPN4", "OPN5", "OPN6", "OPN7", "OPN8", "OPN9", "OPN10"]
}

category_colors = {
    "Extraversión": "#1f77b4",
    "Inestabilidad emocional": "#ff7f0e",
    "Amabilidad": "#2ca02c",
    "Responsabilidad": "#d62728",
    "Apertura a la experiencia": "#9467bd"
}

# Inicializar estado de la sesión
if "responses" not in st.session_state:
    st.session_state.responses = {}
    st.session_state.previous_responses = {}

# Calcular el progreso
if categories:
    total_questions = sum(len(qs) for qs in categories.values())
    completed_questions = len([resp for resp in st.session_state.responses.values() if resp != "Seleccione una opción"])
    progress = completed_questions / total_questions if total_questions > 0 else 0

    st.progress(progress)
    st.markdown(f"""
        <div style="text-align: center; color: #666;">
            Progreso: {completed_questions}/{total_questions} preguntas respondidas ({int(progress * 100)}%)
        </div>
    """, unsafe_allow_html=True)

# Crear pestañas para las categorías
tabs = st.tabs(list(categories.keys()))

for idx, (category, q_keys) in enumerate(categories.items()):
    with tabs[idx]:
        st.markdown(f"""
            <div class="category-title" style="background-color: {category_colors[category]}20;">
                <h2 style="color: {category_colors[category]};">{category}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        for q_key in q_keys:
            st.markdown(f"""
                <div class="question-container">
                    {questions[q_key]}
                </div>
            """, unsafe_allow_html=True)
            
            previous_value = st.session_state.responses.get(q_key, "Seleccione una opción")
            
            response = st.selectbox(
                "Seleccione una opción",
                ["Seleccione una opción", "Totalmente en desacuerdo", "En desacuerdo", "Neutral", "De acuerdo", "Totalmente de acuerdo"],
                key=q_key,
                index=0 if previous_value == "Seleccione una opción" else ["Seleccione una opción", "Totalmente en desacuerdo", "En desacuerdo", "Neutral", "De acuerdo", "Totalmente de acuerdo"].index(previous_value),
                label_visibility="collapsed"
            )
            
            if response != "Seleccione una opción":
                st.session_state.responses[q_key] = response
            elif q_key in st.session_state.responses and response == "Seleccione una opción":
                del st.session_state.responses[q_key]
            
            if (previous_value == "Seleccione una opción" and response != "Seleccione una opción") or (previous_value != response):
                st.session_state.previous_responses = dict(st.session_state.responses)
                st.rerun()

# Botón de predicción
if st.button("📊 Realizar predicción", type="primary", use_container_width=True):
    if len(st.session_state.responses) > 0:
        with st.spinner("Analizando respuestas..."):
            response_mapping = {
                "Totalmente en desacuerdo": 1,
                "En desacuerdo": 2,
                "Neutral": 3,
                "De acuerdo": 4,
                "Totalmente de acuerdo": 5
            }
            
            data = []
            for q_key in questions.keys():
                response = st.session_state.responses.get(q_key, "Neutral")
                data.append(response_mapping[response])
            
            try:
                # Sacar nombres de las columnas para añadirlas al modelo
                feature_names = list(questions.keys())

                data_df = pd.DataFrame([data], columns=feature_names)

                prediction = model.predict([data])

                result = category_mapping[str(prediction[0])]
                
                st.markdown("""
                    <div style="background-color: #f0f2f6; padding: 2rem; border-radius: 0.5rem; margin: 2rem 0;">
                        <h2 style="color: #1f77b4; text-align: center;">🎉 Resultados del Análisis</h2>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                    <div style="background-color: #d4edda; color: #155724; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;">
                        <h2 style="text-align: center; font-size: 1.5rem;">🎉 Su tipo de personalidad es: {result}</h2>
                    </div>
                """, unsafe_allow_html=True)
                
                # Definir las descripciones de personalidad
                personality_descriptions = {
                    "Abierto a la experiencia": "La apertura a la experiencia es un aprecio general por el arte, la emoción, la aventura, las ideas inusuales, la imaginación, la curiosidad y la variedad de experiencias. Las personas abiertas a la experiencia son intelectualmente curiosas, abiertas a las emociones, sensibles a la belleza y dispuestas a probar cosas nuevas. Tienden a ser, en comparación con las personas cerradas, más creativas y más conscientes de sus sentimientos. También son más propensas a tener creencias poco convencionales. Además, se dice que las personas muy abiertas persiguen la autorrealización buscando experiencias intensas y eufóricas.",
                    
                    "Responsable": "La responsabilidad es una tendencia a la autodisciplina, a actuar con diligencia y a esforzarse por conseguir logros a pesar de las medidas o las expectativas externas. Está relacionada con el nivel de control, regulación y dirección de los impulsos de las personas. Un alto grado de responsabilidad o escrupulosidad suele percibirse como una persona obstinada y centrada. La baja responsabilidad se asocia con la flexibilidad y la espontaneidad, pero también puede aparecer como dejadez y falta de fiabilidad. Un nivel alto de responsabilidad indica una preferencia por el comportamiento planificado en lugar del espontáneo. El nivel medio de responsabilidad aumenta entre los adultos jóvenes y disminuye entre los adultos mayores.",
                    
                    "Extrovertido": "La extraversión se caracteriza por la amplitud de actividades (en contraposición a la profundidad), la urgencia de actividades/situaciones externas y la creación de energía a partir de medios externos. Este rasgo se caracteriza por un fuerte compromiso con el mundo exterior. Los extrovertidos disfrutan interactuando con la gente y a menudo se les percibe como personas enérgicas. Suelen ser entusiastas y estar orientados a la acción. Poseen una gran visibilidad de grupo, les gusta hablar y hacerse valer. Los extrovertidos pueden parecer más dominantes en entornos sociales, a diferencia de los introvertidos en ese entorno.",
                    
                    "Amable": "La amabilidad es la preocupación general por la armonía social. Las personas agradables valoran llevarse bien con los demás. Suelen ser consideradas, amables, generosas, confiadas y dignas de confianza, serviciales y dispuestas a comprometer sus intereses con los demás. También tienen una visión optimista de la naturaleza humana. Las personas desagradables anteponen el interés propio a llevarse bien con los demás. Por lo general, no se preocupan por el bienestar de los demás y son menos propensos a sacrificarse por los demás.",
                    
                    "Inestable emocionalmente": "La inestabilidad emocional o neuroticismo es la tendencia a tener fuertes emociones negativas, como ira, ansiedad o depresión. Las personas neuróticas son emocionalmente reactivas y vulnerables al estrés. Son más propensas a interpretar situaciones ordinarias como amenazantes. Pueden percibir frustraciones menores como irremediablemente difíciles. También tienden a ser superficiales en la forma de expresar sus emociones. Sus reacciones emocionales negativas tienden a permanecer durante periodos de tiempo inusualmente largos, lo que significa que a menudo están de mal humor."
                }
                
                # Mostrar la descripción correspondiente con estilo mejorado
                description_html = f"""
                    <div style="
                        background-color: white;
                        padding: 2rem;
                        border-radius: 1rem;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        margin: 2rem 0;
                        border-left: 5px solid #1f77b4;
                    ">
                        <div style="
                            display: flex;
                            align-items: center;
                            margin-bottom: 1rem;
                            border-bottom: 2px solid #f0f2f6;
                            padding-bottom: 1rem;
                        ">
                            <span style="
                                font-size: 2rem;
                                margin-right: 1rem;
                            ">🔍</span>
                            <h3 style="
                                margin: 0;
                                color: #1f77b4;
                                font-size: 1.5rem;
                            ">Análisis Detallado de tu Personalidad</h3>
                        </div>
                        <div style="
                            line-height: 1.6;
                            color: #2c3e50;
                            font-size: 1.1rem;
                            text-align: justify;
                            margin-bottom: 1.5rem;
                        ">
                            {personality_descriptions[result]}
                        </div>
                        <div style="
                            margin-top: 1.5rem;
                            padding-top: 1rem;
                            border-top: 2px solid #f0f2f6;
                            font-size: 0.9rem;
                            color: #666;
                            text-align: center;
                        ">
                            💡 Esta descripción se basa en el análisis de tus respuestas al cuestionario
                        </div>
                    </div>
                """

                st.markdown(description_html, unsafe_allow_html=True)

                # Calcular puntuaciones para el CSV
                results_df = pd.DataFrame({
                    "Categoría": list(categories.keys()),
                    "Puntuación": [sum(data[i:i+10])/10 for i in range(0, len(data), 10)]
                })

                # Botón de descarga
                button_style = """
                    <style>
                    div.stDownloadButton > button {
                        padding: 12px 24px;
                        font-size: 16px;
                    }
                    </style>
                """
                st.markdown(button_style, unsafe_allow_html=True)

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
        st.warning("Por favor, responda al menos una pregunta antes de continuar.")

# Pie de página
st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0; border-top: 1px solid #eee; margin-top: 2rem;">
        <p>Desarrollado con ❤️ por:</br>Hugo Peralta</br>Adrian Perogil</br>Natalie Pilkington</p>
        <p class="small-text">Versión 1.1.0</p>
    </div>
""", unsafe_allow_html=True)