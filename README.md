Fitness Data Engine v1.0
Backend & Analytics para Control de Cargas Progresivas
Como estudiante de Ingeniería Informática y Data Analyst, desarrollé esta herramienta para resolver un problema común en el entrenamiento de fuerza: la dispersión de datos. Este software no solo registra pesos, sino que proyecta el crecimiento del atleta basándose en su desempeño histórico.

El Problema y la Solución
Muchos trackers son visualmente atractivos pero técnicamente pobres en el manejo de datos. Este motor está diseñado para:

Normalizar el input: Manejo de errores en ingresos de peso (puntos vs comas).

Análisis Multidimensional: Separación de lógica de entrenamiento y evolución antropométrica (IMC).

Automatización de Reportes: Generación de archivos Excel con segmentación por Grupo Muscular para facilitar el filtrado y análisis posterior.

Stack Técnico
Lenguaje: Python 3.x

GUI: CustomTkinter (Interfaz moderna con soporte para Dark Mode).

Data Science: Pandas (Motor de procesamiento para exportación analítica).

Persistencia Actual: JSON (Estructura de objetos planos).

Próximo Milestone: Migración completa a SQL para integridad relacional.

Funcionalidades Clave
Carga Progresiva Inteligente: El sistema calcula automáticamente un incremento del 2.5% al 5% basado en tu última sesión efectiva.

Tracking de Composición: Registro histórico de peso con cálculo automático de categoría de IMC.

Exportación Profesional: Genera un archivo .xlsx con hojas separadas para entrenamientos y evolución física, optimizado para ser usado en herramientas de BI o Excel avanzado.

🛠️ Estructura del Proyecto
models.py: Lógica de negocio y procesamiento de datos (OOP).

gui.py: Interfaz de usuario y manejo de eventos.

utils.py: Funciones auxiliares de seguridad (Hashing de PIN) y validación.

config.py: Diccionarios maestros de ejercicios y grupos musculares.
