# Aplicación web con modelo de IA integrado
### Realizado por . . .

- Natalie Pilkington
- Hugo Peralta Muñoz
- Adrián Perogil Fernández

# Proyecto Personality Predictor
### Enlace a la presentación para la exposición
[Presentación](https://www.canva.com/design/DAGbyrJpXHA/mmlnCxcHjKr8kH55TkmvtA/edit)

### Enlace a la aplicación web
[Web](https://apwebia.streamlit.app/)

### Video de la aplicación en vivo (Sin sonido)
[Video](https://drive.google.com/file/d/19uxpKlPufJ3KG7Dhn80NsPi0SaAPkNZu/view?usp=sharing)

### Colab donde se entrenó el modelo
[Colab](https://github.com/imchopi/APWEB_Modelo_IA_Intregrado/blob/main/train_personality_model.ipynb)

Este proyecto es una aplicación web que predice rasgos de personalidad basándose en las respuestas del usuario a una serie de preguntas.

Dichas preguntas están basadas en la Teoría del Big Five ( Extroversión, Amabilidad, Escrupulosidad, Estabilidad emocional y Apertura a la experiencia). 

Utiliza un modelo de aprendizaje automático para realizar las predicciones y está construido con `Streamlit`.

## Uso

- Puedes usar directamente la página hosteada en `Streamlit`, para realizar la encuesta y recibir una predicción: <a>https://apwebia.streamlit.app/</a> o instalar la app de forma local.

## Instalación de la app de forma local

1. Clona el repositorio:
    ```sh
    git clone https://github.com/imchopi/APWEB_Modelo_IA_Intregrado
    cd APWEB_Modelo_IA_Intregrado
    ```
> [!IMPORTANT]
> Para realizar el siguiente paso necesitarás tener instalado docker. Podrás hacerlo desde su página oficial: <a>https://docs.docker.com/engine/install/</a>

2. **Docker**: Puedes usar Docker para ejecutar la aplicación en un contenedor. Construye la imagen y ejecuta el contenedor con:
    ```sh
    docker-compose up
    ```

Tras esto podrás dirigirte a tu navegador y buscar la siguiente dirección: `http://localhost:8501`

Aquí podrás ver de forma local la aplicación `Streamlit`, hosteada en tu imagen docker de forma local.

### Entrenamiento del Modelo

Los datos para entrenar el modelo lo sacamos del siguiente dataset de `Kaggle`:  
<a>https://www.kaggle.com/datasets/tunguz/big-five-personality-test/data</a>

Para entrenar el modelo de personalidad, sigue los pasos en el cuaderno Jupyter `train_personality_model.ipynb`. Este cuaderno incluye la descarga de datos, preprocesamiento y entrenamiento del modelo.

Puedes modificar los parámetros del modelo para buscar resultados distintos.


