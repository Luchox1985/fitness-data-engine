import customtkinter as ctk
from tkinter import messagebox
import os, subprocess
from models import Atleta
from database import cargar_db, guardar_db
from utils import generar_hash, validar_formato_usuario
import config

ctk.set_appearance_mode("dark")

class AppFitness(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Fitness Analytics Pro v17.1")
        self.geometry("600x850")
        self.db = cargar_db()
        self.usuario_actual = None
        self.ventana_activa = None
        self.render_inicio()

    def refrescar(self):
        for w in self.winfo_children(): w.destroy()

    def abrir_modal(self, titulo, ancho=450, alto=600):
        if self.ventana_activa and self.ventana_activa.winfo_exists():
            self.ventana_activa.lift(); self.ventana_activa.focus_force()
            return None
        win = ctk.CTkToplevel(self)
        win.title(titulo); win.geometry(f"{ancho}x{alto}")
        win.transient(self); win.grab_set(); win.lift(); win.focus_force()
        self.ventana_activa = win
        return win

    def render_inicio(self):
        self.refrescar()
        ctk.CTkLabel(self, text="GYM ANALYTICS", font=("Arial", 30, "bold")).pack(pady=60)
        self.u_in = ctk.CTkEntry(self, placeholder_text="ID Usuario", width=250); self.u_in.pack(pady=10)
        self.p_in = ctk.CTkEntry(self, placeholder_text="PIN", show="*", width=250); self.p_in.pack(pady=10)
        ctk.CTkButton(self, text="Entrar", command=self.login).pack(pady=20)
        
        f_b = ctk.CTkFrame(self, fg_color="transparent"); f_b.pack(pady=20)
        ctk.CTkButton(f_b, text="Registrar Atleta", width=120, command=self.modal_registro).pack(side="left", padx=5)
        ctk.CTkButton(f_b, text="Borrar Perfil", width=120, fg_color="#c0392b", command=self.borrar_perfil).pack(side="left", padx=5)

    def login(self):
        uid, pin = self.u_in.get().lower().strip(), self.p_in.get()
        if uid in self.db and generar_hash(pin) == self.db[uid].pin:
            self.usuario_actual = self.db[uid]
            # Asegura que existan los campos de IMC en perfiles viejos
            if not hasattr(self.usuario_actual, 'historial_evolutivo'):
                self.usuario_actual.historial_evolutivo = []
            self.render_dashboard()
        else: messagebox.showerror("Error", "ID o PIN incorrectos")

    def render_dashboard(self):
        self.refrescar()
        u = self.usuario_actual
        f = ctk.CTkFrame(self); f.pack(pady=20, fill="x", padx=30)
        ctk.CTkLabel(f, text=f"ATLETA: {u.nombre.upper()}", font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkLabel(f, text=f"IMC: {u.calcular_imc()} ({u.obtener_categoria()})", text_color="#3498db").pack()

        ctk.CTkButton(self, text="Registrar Sesión 🏋️", command=self.modal_entrenamiento).pack(pady=10)
        ctk.CTkButton(self, text="Ruta de Cargas 📋", fg_color="#d35400", command=self.modal_mapa_ruta).pack(pady=10)
        ctk.CTkButton(self, text="Actualizar Peso ⚖️", command=self.modal_peso).pack(pady=10)
        ctk.CTkButton(self, text="Exportar Excel 📊", fg_color="#1f6f44", command=self.exportar).pack(pady=10)
        ctk.CTkButton(self, text="Cerrar Sesión", fg_color="gray", command=self.render_inicio).pack(pady=30)

    def modal_entrenamiento(self):
        win = self.abrir_modal("Nuevo Registro", alto=500)
        if not win: return
        cb_g = ctk.CTkComboBox(win, values=config.GRUPOS_MUSCULARES, width=250); cb_g.pack(pady=10)
        cb_e = ctk.CTkComboBox(win, values=[], width=250); cb_e.pack(pady=10)
        
        def up(c):
            l = config.EJERCICIOS_POR_GRUPO.get(c, []); cb_e.configure(values=l)
            if l: cb_e.set(l[0])
        cb_g.configure(command=up); up(config.GRUPOS_MUSCULARES[0])
        
        p_i = ctk.CTkEntry(win, placeholder_text="Peso (kg)"); p_i.pack(pady=5)
        r_i = ctk.CTkEntry(win, placeholder_text="Reps"); r_i.pack(pady=5)
        s_i = ctk.CTkEntry(win, placeholder_text="Series"); s_i.pack(pady=5)

        def guardar():
            try:
                msg = self.usuario_actual.registrar_entrenamiento(cb_g.get(), cb_e.get(), p_i.get(), r_i.get(), s_i.get())
                guardar_db(self.db); win.destroy(); messagebox.showinfo("OK", msg); self.render_dashboard()
            except: messagebox.showerror("Error", "Ingresa números válidos")
        ctk.CTkButton(win, text="Guardar", command=guardar).pack(pady=20)

    def modal_mapa_ruta(self):
        win = self.abrir_modal("Progresión", ancho=500, alto=450)
        if not win: return
        cb_g = ctk.CTkComboBox(win, values=config.GRUPOS_MUSCULARES, width=250); cb_g.pack(pady=10)
        cb_e = ctk.CTkComboBox(win, values=[], width=250); cb_e.pack(pady=10)
        def up(c):
            l = config.EJERCICIOS_POR_GRUPO.get(c, []); cb_e.configure(values=l)
            if l: cb_e.set(l[0])
        cb_g.configure(command=up); up(config.GRUPOS_MUSCULARES[0])

        f_t = ctk.CTkFrame(win, fg_color="transparent"); f_t.pack(pady=20)

        def calcular():
            for w in f_t.winfo_children(): w.destroy()
            proy = self.usuario_actual.obtener_proyeccion(cb_e.get())
            if proy["min"] == 0: return messagebox.showinfo("!", "Sin datos previos")
            
            ctk.CTkLabel(f_t, text="CONCEPTO", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=20)
            ctk.CTkLabel(f_t, text="CARGA (KG)", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=20)
            
            filas = [("Mínimo Sugerido", proy['min']), ("Máximo Sugerido", proy['max'])]
            for r, (c, v) in enumerate(filas, 1):
                ctk.CTkLabel(f_t, text=c).grid(row=r, column=0, pady=5)
                ctk.CTkLabel(f_t, text=f"{v} kg", text_color="#2ecc71", font=("Arial", 12, "bold")).grid(row=r, column=1)
        ctk.CTkButton(win, text="Ver Proyección", command=calcular).pack(pady=10)

    def modal_peso(self):
        res = ctk.CTkInputDialog(text="Nuevo peso (kg):", title="Peso").get_input()
        if res:
            try:
                val = float(res.replace(",", ".").strip())
                msg = self.usuario_actual.actualizar_peso(val)
                guardar_db(self.db); self.render_dashboard(); messagebox.showinfo("Éxito", msg)
            except: messagebox.showerror("Error", "Número inválido")

    def exportar(self):
        ok, path = self.usuario_actual.generar_excel()
        if ok:
            messagebox.showinfo("Excel", f"Reporte generado: {path}")
            try:
                if os.name == 'nt': os.startfile(path)
                else: subprocess.call(['open' if os.uname().sysname == 'Darwin' else 'xdg-open', path])
            except: pass
        else: messagebox.showerror("Error", path)

    def modal_registro(self):
        win = self.abrir_modal("Registro", alto=750)
        if not win: return
        ctk.CTkLabel(win, text="PASO 1: ID", font=("Arial", 12, "bold")).pack(pady=10)
        u_e = ctk.CTkEntry(win, placeholder_text="ej: lv25"); u_e.pack()
        btn_v = ctk.CTkButton(win, text="Validar ID"); btn_v.pack(pady=5)
        ctk.CTkFrame(win, height=2, fg_color="gray30", width=350).pack(pady=15)
        
        inputs = {}
        for k, lbl in [("nom", "Nombre:"), ("pes", "Peso:"), ("alt", "Altura:"), ("pin", "PIN:")]:
            ctk.CTkLabel(win, text=lbl).pack(anchor="w", padx=50)
            e = ctk.CTkEntry(win, width=320, state="disabled", fg_color="gray25")
            if k == "pin": e.configure(show="*")
            e.pack(pady=5); inputs[k] = e
        btn_f = ctk.CTkButton(win, text="Crear", state="disabled"); btn_f.pack(pady=20)

        def validar():
            uid = u_e.get().lower().strip()
            if not validar_formato_usuario(uid) or uid in self.db: return messagebox.showerror("!", "ID en uso")
            u_e.configure(state="disabled"); btn_v.configure(text="✅", state="disabled")
            for x in inputs.values(): x.configure(state="normal")
            btn_f.configure(state="normal", fg_color="#2ecc71")
        
        def finalizar():
            uid = u_e.get().lower().strip()
            self.db[uid] = Atleta(inputs["nom"].get(), inputs["pes"].get(), inputs["alt"].get(), generar_hash(inputs["pin"].get()))
            guardar_db(self.db); win.destroy(); messagebox.showinfo("OK", "Creado")
        
        btn_v.configure(command=validar); btn_f.configure(command=finalizar)

    def borrar_perfil(self):
        d = ctk.CTkInputDialog(text="ID a borrar:", title="Eliminar").get_input()
        if d and d.lower().strip() in self.db:
            if messagebox.askyesno("?", f"¿Borrar {d}?"):
                del self.db[d.lower().strip()]; guardar_db(self.db); self.render_inicio()

if __name__ == "__main__":
    app = AppFitness(); app.mainloop()