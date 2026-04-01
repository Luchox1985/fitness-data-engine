import hashlib
def generar_hash(txt): return hashlib.sha256(str(txt).encode()).hexdigest()
def validar_formato_usuario(uid): return len(uid) == 4 and uid[:2].isalpha() and uid[2:].isdigit()