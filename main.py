# main.py
from database import cargar_db, guardar_db
from models import Atleta
from config import EJERCICIOS_BASE
from utils import *

def recuperar_pin(db):
    """Flujo de Ciberseguridad para recuperación de acceso."""
    limpiar_pantalla()
    print("--- RECUPERACIÓN DE ACCESO ---")
    uid = input("Ingrese su nombre de usuario: ").strip().lower()
    
    if uid not in db:
        input("[!] El usuario no existe en el sistema.")
        return

    u = db[uid]
    print(f"\nPregunta de seguridad: {u.pregunta}")
    resp_intento = input("Respuesta: ").strip().lower()

    # Validación mediante hash para no comparar texto plano
    if generar_hash(resp_intento) == u.respuesta:
        print("\n[OK] Identidad verificada.")
        while True:
            nuevo_pin = input_obligatorio("Ingrese nuevo PIN (4 dígitos): ")
            if len(nuevo_pin) == 4 and nuevo_pin.isdigit():
                hash_n = generar_hash(nuevo_pin)
                # Regla de Negocio: No repetir PINs recientes
                if hash_n in u.historial_pin:
                    print("[!] Por seguridad, no puedes usar un PIN antiguo.")
                else:
                    u.pin = hash_n
                    u.historial_pin.append(hash_n)
                    if len(u.historial_pin) > 5: u.historial_pin.pop(0)
                    guardar_db(db)
                    input("[OK] PIN actualizado con éxito. Ya puedes iniciar sesión.")
                    break
            else:
                print("[!] El PIN debe ser de 4 números.")
    else:
        input("[!] Respuesta incorrecta. Acceso denegado.")

def flujo_registro(db):
    """Registro amigable con validación de disponibilidad."""
    limpiar_pantalla()
    print("--- REGISTRO DE NUEVO ATLETA ---")
    
    # 1. Validación de Disponibilidad de Usuario
    while True:
        new_uid = input("Elige tu nombre de usuario (ej: jara25): ").strip().lower()
        if not validar_formato_usuario(new_uid):
            print("[!] Formato inválido (debe tener 2 letras y 2 números).")
            continue
        if new_uid in db:
            print(f"[!] Lo siento, '{new_uid}' ya está en uso. Intenta con otro.")
        else:
            print(f"[OK] ¡'{new_uid}' está disponible!")
            break

    # 2. Datos Personales
    nom = input_obligatorio("Nombre completo: ")
    try:
        p = float(input_obligatorio("Peso actual (kg): "))
        a = float(input_obligatorio("Altura (m): "))
    except ValueError:
        input("[!] Error: Peso y altura deben ser números. Reiniciando registro..."); return

    # 3. Configuración de Seguridad
    pin = input_obligatorio("Define tu PIN de 4 dígitos: ")
    while not (len(pin) == 4 and pin.isdigit()):
        pin = input_obligatorio("[!] PIN inválido. Ingresa 4 números: ")
    
    print("\n--- CONFIGURACIÓN DE RECUPERACIÓN ---")
    preg = input_obligatorio("Pregunta de seguridad (ej: ¿Nombre de tu gato?): ")
    resp = input_obligatorio("Respuesta de seguridad: ").lower()

    # 4. Creación de Objeto y Persistencia
    nuevo_atleta = Atleta(
        nom, p, a, 
        generar_hash(pin), 
        preg, 
        generar_hash(resp)
    )
    nuevo_atleta.actualizar_peso(p) # Inicia el historial
    db[new_uid] = nuevo_atleta
    guardar_db(db)
    input(f"\n[OK] ¡Bienvenido {nom}! Registro completado exitosamente.")

def ver_evolucion(u):
    """Módulo Analítico de Progreso."""
    while True:
        limpiar_pantalla()
        print(f"--- ANALYTICS DE {u.nombre.upper()} ---")
        print("1. Historial Físico (Peso/IMC)\n2. Evolución de Cargas\n3. Volver")
        op = input("\nSeleccione > ")
        
        if op == "1":
            print(f"\n{'FECHA':10} | {'PESO':6} | {'IMC':5} | {'ESTADO'}")
            print("-" * 40)
            for h in u.historial_peso:
                print(f"{h['fecha']:10} | {h['peso']:4}kg | {h['imc']:5} | {u.obtener_categoria_imc()}")
            input("\nEnter...")
        elif op == "2":
            # (Aquí va la lógica de volumen que ya teníamos consolidada)
            input("\nMostrando gráficos de volumen... [Enter]")
        elif op == "3": break

def main():
    while True:
        db = cargar_db()
        limpiar_pantalla()
        print("=== FITNESS PRO ANALYTICS v6.7 ===")
        print("1. Login")
        print("2. Registrarse (Nuevo Usuario)")
        print("3. Olvidé mi PIN")
        print("4. Salir")
        
        op = input("\nAcción > ")
        
        if op == "1":
            uid = input("Usuario: ").strip().lower()
            pin = input("PIN: ")
            if uid in db and generar_hash(pin) == db[uid].pin:
                panel_atleta(db, uid)
            else:
                input("[!] Credenciales incorrectas.")
        elif op == "2":
            flujo_registro(db)
        elif op == "3":
            recuperar_pin(db)
        elif op == "4":
            print("Saliendo del sistema..."); break

def panel_atleta(db, uid):
    u = db[uid]
    while True:
        limpiar_pantalla()
        print(f"--- DASHBOARD: {u.nombre.upper()} ---")
        print(f"Estado Actual: {u.peso_actual}kg | IMC: {u.calcular_imc()}")
        print("-" * 35)
        print("1. Registrar Entrenamiento\n2. Ver Evolución\n3. Actualizar Peso\n4. Logout")
        op = input("\nSeleccione > ")
        
        if op == "1":
            # Flujo de registro de ejercicios
            pass 
        elif op == "2":
            ver_evolucion(u)
        elif op == "3":
            # Actualización de peso
            pass
        elif op == "4": break

if __name__ == "__main__":
    main()