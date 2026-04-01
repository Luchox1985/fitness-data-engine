import pandas as pd
from datetime import datetime
from typing import List, Dict, Union, Tuple

class Atleta:
    """
    Clase que gestiona la lógica de negocio, cálculos de rendimiento 
    y persistencia de datos para el análisis de entrenamiento.
    """
    def __init__(self, nombre: str, peso: float, altura: float, pin: str):
        self.nombre = nombre
        self.pin = pin
        
        # Normalización de medidas físicas
        self.peso_actual = float(peso)
        alt_raw = float(altura)
        self.altura = alt_raw / 100 if alt_raw > 3 else alt_raw
        
        # Estructuras de datos para series de tiempo
        self.entrenamientos: List[Dict] = []
        self.historial_evolutivo: List[Dict] = []
        
        # Registro inicial de estado físico
        self._registrar_estado_fisico()

    def _registrar_estado_fisico(self):
        """Metodo privado para el tracking de composición corporal."""
        self.historial_evolutivo.append({
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "peso_kg": self.peso_actual,
            "imc": self.calcular_imc()
        })

    def calcular_imc(self) -> float:
        if self.altura <= 0: return 0.0
        return round(self.peso_actual / (self.altura ** 2), 2)

    def obtener_categoria(self) -> str:
        imc = self.calcular_imc()
        if imc < 18.5: return "Bajo Peso"
        if imc < 25:   return "Normal"
        if imc < 30:   return "Sobrepeso"
        return "Obesidad"

    def registrar_entrenamiento(self, grupo: str, ejercicio: str, peso: str, reps: str, series: str) -> str:
        try:
            p, r, s = float(peso), int(reps), int(series)
            data = {
                "fecha": datetime.now().strftime("%d/%m/%Y"),
                "grupo_muscular": grupo.upper(),
                "ejercicio": ejercicio,
                "peso_kg": p,
                "reps": r,
                "series": s,
                "volumen_total": round(p * r * s, 2)
            }
            self.entrenamientos.append(data)
            return f"Log: {ejercicio} registrado correctamente."
        except ValueError:
            raise ValueError("Los datos de entrenamiento deben ser numéricos.")

    def actualizar_peso(self, nuevo_peso: float) -> str:
        self.peso_actual = nuevo_peso
        self._registrar_estado_fisico()
        return f"Update: Peso actualizado a {self.peso_actual}kg."

    def obtener_proyeccion(self, ejercicio: str) -> Dict[str, float]:
        """Calcula la sobrecarga progresiva basada en el último registro."""
        logs = [e for e in self.entrenamientos if e['ejercicio'] == ejercicio]
        if not logs:
            return {"min": 0.0, "max": 0.0}
        
        # Compatibilidad con legacy data ('peso' vs 'peso_kg')
        ultimo = logs[-1]
        base_peso = ultimo.get('peso_kg', ultimo.get('peso', 0))
        
        return {
            "min": round(base_peso * 1.025, 2),
            "max": round(base_peso * 1.05, 2)
        }

    def generar_excel(self) -> Tuple[bool, str]:
        """Exporta dataframes limpios con múltiples hojas para análisis."""
        try:
            filename = f"Analisis_{self.nombre.replace(' ', '_')}.xlsx"
            
            # Procesamiento de DataFrames
            df_gym = pd.DataFrame(self.entrenamientos)
            df_imc = pd.DataFrame(self.historial_evolutivo)

            # Reordenamiento lógico para análisis de datos
            cols_gym = ['fecha', 'grupo_muscular', 'ejercicio', 'peso_kg', 'reps', 'series', 'volumen_total']
            if not df_gym.empty:
                df_gym = df_gym[[c for c in cols_gym if c in df_gym.columns]]

            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df_gym.to_excel(writer, sheet_name='Data_Cargas', index=False)
                df_imc.to_excel(writer, sheet_name='Evolucion_IMC', index=False)
            
            return True, filename
        except Exception as e:
            return False, f"Error en exportación: {str(e)}"