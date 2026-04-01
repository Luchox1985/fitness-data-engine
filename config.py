# config.py
DB_FILE = "fitness_data.pkl"

GRUPOS_MUSCULARES = [
    "Piernas", "Bíceps", "Tríceps", "Pecho", "Espalda", "Hombros"
]

EJERCICIOS_POR_GRUPO = {
    "Piernas": ["Sentadilla", "Prensa", "Estocadas", "Peso Muerto", "Extensiones"],
    "Bíceps": ["Curl de Bíceps", "Martillo", "Curl Predicador"],
    "Tríceps": ["Press Francés", "Extensiones en Polea", "Fondos"],
    "Pecho": ["Press Banca", "Press Inclinado", "Aperturas", "Cruces de Polea"],
    "Espalda": ["Dominadas", "Remo con Barra", "Jalón al Pecho", "Pull Over"],
    "Hombros": ["Press Militar", "Vuelos Laterales", "Pájaros", "Frontales"]
}