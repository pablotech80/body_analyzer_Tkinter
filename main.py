import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from calculadora import (
    calcular_tmb, calcular_imc, calcular_porcentaje_grasa,
    calcular_agua_total, interpretar_imc, calcular_peso_saludable,
    calcular_masa_magra, calcular_ffmi, interpretar_ffmi,
    calcular_relacion_cintura_cadera, calcular_calorias_diarias,
    calcular_macronutrientes, interpretar_rcc,
    calcular_ratio_cintura_altura, interpretar_ratio_cintura_altura,
    interpretar_porcentaje_grasa, guardar_datos, recuperar_historial
)
from models import Usuario, Session, engine
from sqlalchemy.orm import sessionmaker


# Configuración de la sesión de la base de datos
Session = sessionmaker(bind=engine)
session = Session()

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis de Composición Corporal")
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz de usuario principal"""
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12, 'bold'))
        style.configure('TLabel', font=('Arial', 12))
        style.configure('TEntry', font=('Arial', 12))

        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.button_frame = ttk.Frame(self.frame, padding="10")
        self.button_frame.grid(row=29, column=0, columnspan=2, sticky=(tk.W, tk.E))

        self.setup_input_fields()
        self.setup_result_labels()
        self.setup_buttons()

    def setup_input_fields(self):
        """Configura los campos de entrada de datos"""
        # Nombre
        ttk.Label(self.frame, text="Nombre Completo:").grid(row=0, column=0, sticky=tk.W)
        self.nombre = tk.StringVar()
        ttk.Entry(self.frame, textvariable=self.nombre).grid(row=0, column=1, sticky=(tk.W, tk.E))

        # Peso
        ttk.Label(self.frame, text="Peso (kg):").grid(row=1, column=0, sticky=tk.W)
        self.peso = tk.StringVar()
        ttk.Entry(self.frame, textvariable=self.peso).grid(row=1, column=1, sticky=(tk.W, tk.E))

        # Altura
        ttk.Label(self.frame, text="Altura (cm):").grid(row=2, column=0, sticky=tk.W)
        self.altura = tk.StringVar()
        ttk.Entry(self.frame, textvariable=self.altura).grid(row=2, column=1, sticky=(tk.W, tk.E))

        # Edad
        ttk.Label(self.frame, text="Edad:").grid(row=3, column=0, sticky=tk.W)
        self.edad = tk.StringVar()
        ttk.Entry(self.frame, textvariable=self.edad).grid(row=3, column=1, sticky=(tk.W, tk.E))

        # Género
        ttk.Label(self.frame, text="Género (H/M):").grid(row=4, column=0, sticky=tk.W)
        self.genero = tk.StringVar()
        self.genero_entry = ttk.Entry(self.frame, textvariable=self.genero)
        self.genero_entry.grid(row=4, column=1, sticky=(tk.W, tk.E))
        self.genero_entry.bind('<KeyRelease>', self.actualizar_panel)

        # Objetivo
        ttk.Label(self.frame, text="Objetivo (mantener/perder/ganar):").grid(row=5, column=0, sticky=tk.W)
        self.objetivo = tk.StringVar()
        self.objetivo_entry = ttk.Entry(self.frame, textvariable=self.objetivo)
        self.objetivo_entry.grid(row=5, column=1, sticky=(tk.W, tk.E))
        self.objetivo_entry.bind('<KeyRelease>', self.actualizar_macros)

        # Macronutrientes
        ttk.Label(self.frame, text="Proteína (%):").grid(row=6, column=0, sticky=tk.W)
        self.proteina = tk.StringVar()
        ttk.Entry(self.frame, textvariable=self.proteina).grid(row=6, column=1, sticky=(tk.W, tk.E))

        ttk.Label(self.frame, text="Carbohidrato (%):").grid(row=7, column=0, sticky=tk.W)
        self.carbohidrato = tk.StringVar()
        ttk.Entry(self.frame, textvariable=self.carbohidrato).grid(row=7, column=1, sticky=(tk.W, tk.E))

        ttk.Label(self.frame, text="Grasa (%):").grid(row=8, column=0, sticky=tk.W)
        self.grasa = tk.StringVar()
        ttk.Entry(self.frame, textvariable=self.grasa).grid(row=8, column=1, sticky=(tk.W, tk.E))

        # Medidas corporales
        ttk.Label(self.frame, text="Circunferencia de Cintura (cm):").grid(row=9, column=0, sticky=tk.W)
        self.cintura = tk.StringVar()
        ttk.Entry(self.frame, textvariable=self.cintura).grid(row=9, column=1, sticky=(tk.W, tk.E))

        self.cadera_label = ttk.Label(self.frame, text="Circunferencia de Cadera (cm):")
        self.cadera_label.grid(row=10, column=0, sticky=tk.W)
        self.cadera = tk.StringVar()
        self.cadera_entry = ttk.Entry(self.frame, textvariable=self.cadera)
        self.cadera_entry.grid(row=10, column=1, sticky=(tk.W, tk.E))

        ttk.Label(self.frame, text="Circunferencia de Cuello (cm):").grid(row=11, column=0, sticky=tk.W)
        self.cuello = tk.StringVar()
        ttk.Entry(self.frame, textvariable=self.cuello).grid(row=11, column=1, sticky=(tk.W, tk.E))

    def setup_result_labels(self):
        """Configura las etiquetas para mostrar los resultados"""
        ttk.Label(self.frame, text="Resultados:").grid(row=12, column=0, sticky=tk.W)

        self.resultado_tmb = tk.StringVar()
        ttk.Label(self.frame, textvariable=self.resultado_tmb).grid(row=13, column=0, columnspan=2, sticky=(tk.W, tk.E))

        self.resultado_imc = tk.StringVar()
        ttk.Label(self.frame, textvariable=self.resultado_imc).grid(row=14, column=0, columnspan=2, sticky=(tk.W, tk.E))

        self.resultado_porcentaje_grasa = tk.StringVar()
        ttk.Label(self.frame, textvariable=self.resultado_porcentaje_grasa).grid(row=15, column=0, columnspan=2,
                                                                                 sticky=(tk.W, tk.E))

        self.resultado_peso_grasa = tk.StringVar()
        ttk.Label(self.frame, textvariable=self.resultado_peso_grasa).grid(row=16, column=0, columnspan=2,
                                                                           sticky=(tk.W, tk.E))

        self.resultado_masa_muscular = tk.StringVar()
        ttk.Label(self.frame, textvariable=self.resultado_masa_muscular).grid(row=17, column=0, columnspan=2,
                                                                              sticky=(tk.W, tk.E))

        self.resultado_agua_total = tk.StringVar()
        ttk.Label(self.frame, textvariable=self.resultado_agua_total).grid(row=18, column=0, columnspan=2,
                                                                           sticky=(tk.W, tk.E))

        self.resultado_ffmi = tk.StringVar()
        ttk.Label(self.frame, textvariable=self.resultado_ffmi).grid(row=19, column=0, columnspan=2,
                                                                     sticky=(tk.W, tk.E))

        self.interpretacion_ffmi = tk.StringVar()
        ttk.Label(self.frame, textvariable=self.interpretacion_ffmi).grid(row=20, column=0, columnspan=2,
                                                                          sticky=(tk.W, tk.E))

        self.interpretacion_imc = tk.StringVar()
        ttk.Label(self.frame, textvariable=self.interpretacion_imc).grid(row=21, column=0, columnspan=2,
                                                                         sticky=(tk.W, tk.E))

        self.resultado_peso_saludable = tk.StringVar()
        ttk.Label(self.frame, textvariable=self.resultado_peso_saludable).grid(row=22, column=0, columnspan=2,
                                                                               sticky=(tk.W, tk.E))

        self.resultado_sobrepeso = tk.StringVar()
        ttk.Label(self.frame, textvariable=self.resultado_sobrepeso).grid(row=23, column=0, columnspan=2,
                                                                          sticky=(tk.W, tk.E))

        self.resultado_rcc = tk.StringVar()
        ttk.Label(self.frame, textvariable=self.resultado_rcc).grid(row=24, column=0, columnspan=2, sticky=(tk.W, tk.E))

        self.resultado_ratio_cintura_altura = tk.StringVar()
        ttk.Label(self.frame, textvariable=self.resultado_ratio_cintura_altura).grid(row=25, column=0, columnspan=2,
                                                                                     sticky=(tk.W, tk.E))

        self.resultado_calorias_diarias = tk.StringVar()
        ttk.Label(self.frame, textvariable=self.resultado_calorias_diarias).grid(row=26, column=0, columnspan=2,
                                                                                 sticky=(tk.W, tk.E))

        self.resultado_macronutrientes = tk.StringVar()
        ttk.Label(self.frame, textvariable=self.resultado_macronutrientes).grid(row=27, column=0, columnspan=2,
                                                                                sticky=(tk.W, tk.E))

        self.resultado_salud = tk.StringVar()
        ttk.Label(self.frame, textvariable=self.resultado_salud, wraplength=400).grid(row=28, column=0, columnspan=2,
                                                                                      sticky=(tk.W, tk.E))

    def setup_buttons(self):
        """Configura los botones de la aplicación"""
        ttk.Button(self.button_frame, text="Calcular", command=self.calcular).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(self.button_frame, text="Guardar", command=self.guardar_perfil).grid(row=0, column=1,
                                                                                        sticky=(tk.W, tk.E))
        ttk.Button(self.button_frame, text="Limpiar", command=self.limpiar_campos).grid(row=1, column=0,
                                                                                        sticky=(tk.W, tk.E))
        ttk.Button(self.button_frame, text="Historial", command=self.mostrar_historial).grid(row=1, column=1,
                                                                                             sticky=(tk.W, tk.E))
        ttk.Button(self.button_frame, text="Exportar", command=self.exportar_historial).grid(row=1, column=2,
                                                                                             sticky=(tk.W, tk.E))

    def actualizar_panel(self, event):
        """Actualiza los campos de la interfaz según el género seleccionado"""
        genero_val = self.genero.get().lower()
        if genero_val == 'h':
            self.cadera_label.grid_remove()
            self.cadera_entry.grid_remove()
        else:
            self.cadera_label.grid()
            self.cadera_entry.grid()

    def actualizar_macros(self, event):
        """Actualiza los porcentajes de macronutrientes según el objetivo seleccionado"""
        objetivo_val = self.objetivo.get().lower()
        if objetivo_val == 'mantener':
            self.proteina.set("30")
            self.carbohidrato.set("40")
            self.grasa.set("30")
        elif objetivo_val == 'perder':
            self.proteina.set("40")
            self.carbohidrato.set("40")
            self.grasa.set("20")
        elif objetivo_val == 'ganar':
            self.proteina.set("30")
            self.carbohidrato.set("50")
            self.grasa.set("20")


    def actualizar_macros(self, event):
        """Actualiza los porcentajes de macronutrientes según el objetivo seleccionado"""
        objetivo_val = self.objetivo.get().lower()
        if objetivo_val == 'mantener':
            self.proteina.set("30")
            self.carbohidrato.set("40")
            self.grasa.set("30")
        elif objetivo_val == 'perder':
            self.proteina.set("40")
            self.carbohidrato.set("40")
            self.grasa.set("20")
        elif objetivo_val == 'ganar':
            self.proteina.set("30")
            self.carbohidrato.set("50")
            self.grasa.set("20")

    def calcular(self):
        """Realiza los cálculos de composición corporal y muestra los resultados"""
        if not self.validar_entradas():
            return

        peso_val = float(self.peso.get())
        altura_val = float(self.altura.get())
        edad_val = int(self.edad.get())
        genero_val = self.genero.get().lower()
        cintura_val = float(self.cintura.get())
        cadera_val = float(self.cadera.get()) if genero_val == 'm' else 0.0
        cuello_val = float(self.cuello.get())
        objetivo_val = self.objetivo.get().lower()

        tmb = round(calcular_tmb(peso_val, altura_val, edad_val, genero_val), 2)
        imc = round(calcular_imc(peso_val, altura_val), 2)
        porcentaje_grasa = round(calcular_porcentaje_grasa(cintura_val, cadera_val, cuello_val, altura_val, genero_val),
                                 2)
        peso_grasa = round((porcentaje_grasa / 100) * peso_val, 2)
        masa_magra = round(calcular_masa_magra(peso_val, porcentaje_grasa), 2)
        ffmi = round(calcular_ffmi(masa_magra, altura_val), 2)
        interpretacion_ffmi_val = interpretar_ffmi(ffmi, genero_val)
        agua_total = round(calcular_agua_total(peso_val, altura_val, edad_val, genero_val), 2)
        interpretacion = interpretar_imc(imc, ffmi, genero_val)
        peso_min, peso_max = calcular_peso_saludable(altura_val)
        peso_min, peso_max = round(peso_min, 2), round(peso_max, 2)
        sobrepeso = round(max(0, peso_val - peso_max), 2)
        rcc = round(calcular_relacion_cintura_cadera(cintura_val, cadera_val) if genero_val == 'm' else 0.0, 2)
        interpretacion_rcc_val = interpretar_rcc(rcc, genero_val) if rcc != 0.0 else "N/A"
        ratio_cintura_altura = round(calcular_ratio_cintura_altura(cintura_val, altura_val), 2)
        interpretacion_ratio_cintura_altura_val = interpretar_ratio_cintura_altura(ratio_cintura_altura)
        calorias_diarias = round(calcular_calorias_diarias(tmb, objetivo_val), 2)
        proteinas, carbohidratos, grasas = calcular_macronutrientes(calorias_diarias, objetivo_val)
        proteinas, carbohidratos, grasas = round(proteinas, 2), round(carbohidratos, 2), round(grasas, 2)
        interpretacion_porcentaje_grasa = interpretar_porcentaje_grasa(porcentaje_grasa, genero_val)

        # Actualizar los resultados en la interfaz
        self.resultado_tmb.set(f"TMB: {tmb:.2f} kcal/día")
        self.resultado_imc.set(f"IMC: {imc:.2f}")
        self.resultado_porcentaje_grasa.set(
            f"Porcentaje de Grasa: {porcentaje_grasa:.2f}% ({interpretacion_porcentaje_grasa})")
        self.resultado_peso_grasa.set(f"Peso de Grasa Corporal: {peso_grasa:.2f} kg")
        self.resultado_masa_muscular.set(f"Masa Magra: {masa_magra:.2f} kg")
        self.resultado_agua_total.set(f"Agua Total del Cuerpo: {agua_total:.2f} litros")
        self.resultado_ffmi.set(f"FFMI: {ffmi:.2f}")
        self.interpretacion_ffmi.set(f"Interpretación FFMI: {interpretacion_ffmi_val}")
        self.interpretacion_imc.set(f"Interpretación IMC: {interpretacion}")
        self.resultado_peso_saludable.set(f"Peso Saludable: {peso_min:.2f} kg - {peso_max:.2f} kg")
        self.resultado_sobrepeso.set(f"Sobrepeso: {sobrepeso:.2f} kg")
        self.resultado_rcc.set(f"Relación Cintura/Cadera: {rcc} ({interpretacion_rcc_val})")
        self.resultado_ratio_cintura_altura.set(
            f"Ratio Cintura/Altura: {ratio_cintura_altura:.2f} ({interpretacion_ratio_cintura_altura_val})")
        self.resultado_calorias_diarias.set(f"Calorías Diarias Necesarias: {calorias_diarias:.2f} kcal")
        self.resultado_macronutrientes.set(
            f"Macronutrientes: Proteínas: {proteinas:.2f}g, Carbohidratos: {carbohidratos:.2f}g, Grasas: {grasas:.2f}g")

        # Mensaje de salud basado en el porcentaje de grasa corporal
        if genero_val == 'h':
            if porcentaje_grasa > 26:
                mensaje_salud = "Alto porcentaje de grasa corporal. Se recomienda consultar con un profesional de salud."
            elif porcentaje_grasa < 6:
                mensaje_salud = "Bajo porcentaje de grasa corporal. Se recomienda consultar con un profesional de salud."
            else:
                mensaje_salud = "Porcentaje de grasa corporal dentro del rango normal."
        else:
            if porcentaje_grasa > 32:
                mensaje_salud = "Alto porcentaje de grasa corporal. Se recomienda consultar con un profesional de salud."
            elif porcentaje_grasa < 10:
                mensaje_salud = "Bajo porcentaje de grasa corporal. Se recomienda consultar con un profesional de salud."
            else:
                mensaje_salud = "Porcentaje de grasa corporal dentro del rango normal."

        self.resultado_salud.set(mensaje_salud)

    def validar_entradas(self):
        """Valida que todas las entradas necesarias estén presentes y correctas"""
        try:
            float(self.peso.get())
            float(self.altura.get())
            int(self.edad.get())
            float(self.cintura.get())
            float(self.cuello.get())
            if self.genero.get().lower() == 'm':
                float(self.cadera.get())
        except ValueError:
            messagebox.showerror("Error de entrada", "Por favor, ingrese valores numéricos válidos.")
            return False
        return True

    def guardar_perfil(self):
        """Guarda los datos del cliente en la base de datos"""
        if not self.validar_entradas():
            return

        cliente_data = {
            'nombre': self.nombre.get(),
            'fecha': datetime.now(),
            'peso': float(self.peso.get()),
            'altura': float(self.altura.get()),
            'edad': int(self.edad.get()),
            'genero': self.genero.get().lower(),
            'cintura': float(self.cintura.get()),
            'cadera': float(self.cadera.get()) if self.genero.get().lower() == 'm' else 0.0,
            'cuello': float(self.cuello.get()),
            'tmb': float(self.resultado_tmb.get().split(":")[1].strip().split()[0]),
            'porcentaje_grasa': float(self.resultado_porcentaje_grasa.get().split(":")[1].strip().split("%")[0]),
            'peso_grasa': float(self.resultado_peso_grasa.get().split(":")[1].strip().split()[0]),
            'masa_muscular': float(self.resultado_masa_muscular.get().split(":")[1].strip().split()[0]),
            'agua_total': float(self.resultado_agua_total.get().split(":")[1].strip().split()[0])
        }

        if guardar_datos(cliente_data):
            messagebox.showinfo("Éxito", "Datos del cliente guardados con éxito.")
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", "No se pudieron guardar los datos del cliente.")

    def limpiar_campos(self):
        """Limpia todos los campos de entrada y resultados"""
        for var in [self.nombre, self.peso, self.altura, self.edad, self.genero, self.objetivo,
                    self.proteina, self.carbohidrato, self.grasa, self.cadera, self.cintura, self.cuello]:
            var.set("")
        for var in [self.resultado_tmb, self.resultado_imc, self.resultado_porcentaje_grasa,
                    self.resultado_peso_grasa, self.resultado_masa_muscular, self.resultado_agua_total,
                    self.resultado_ffmi, self.interpretacion_ffmi, self.interpretacion_imc,
                    self.resultado_peso_saludable, self.resultado_sobrepeso, self.resultado_rcc,
                    self.resultado_ratio_cintura_altura, self.resultado_calorias_diarias,
                    self.resultado_macronutrientes, self.resultado_salud]:
            var.set("")

    def mostrar_historial(self):
        """Muestra el historial de clientes guardados en la base de datos"""
        historial_window = tk.Toplevel(self.root)
        historial_window.title("Historial de Clientes")

        tree = ttk.Treeview(historial_window, columns=('Fecha', 'Nombre', 'Altura', 'Peso', 'Porcentaje Grasa'),
                            show='headings')
        tree.heading('Fecha', text='Fecha')
        tree.heading('Nombre', text='Nombre')
        tree.heading('Altura', text='Altura (cm)')
        tree.heading('Peso', text='Peso (kg)')
        tree.heading('Porcentaje Grasa', text='% Grasa')

        tree.column('Fecha', width=100)
        tree.column('Nombre', width=150)
        tree.column('Altura', width=100)
        tree.column('Peso', width=100)
        tree.column('Porcentaje Grasa', width=100)

        historial = recuperar_historial()
        for cliente in historial:
            tree.insert('', 'end', values=(
                cliente.fecha.strftime('%Y-%m-%d'),
                cliente.nombre,
                f"{cliente.altura:.1f}",
                f"{cliente.peso:.1f}",
                f"{cliente.porcentaje_grasa:.1f}"
            ))

        vsb = ttk.Scrollbar(historial_window, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(historial_window, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(column=0, row=0, sticky='nsew')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')

        historial_window.grid_columnconfigure(0, weight=1)
        historial_window.grid_rowconfigure(0, weight=1)

    def exportar_historial(self):
        """Exporta el historial de clientes guardados a un archivo CSV"""
        historial = recuperar_historial()
        with open('historial_clientes.csv', 'w') as file:
            file.write(
                "Nombre,Fecha,Peso,Altura,Edad,Género,Cintura,Cadera,Cuello,TMB,Porcentaje Grasa,Peso Grasa,Masa Muscular,Agua Total\n")
            for cliente in historial:
                file.write(
                    f"{cliente.nombre},{cliente.fecha},{cliente.peso},{cliente.altura},{cliente.edad},{cliente.genero},{cliente.cintura},{cliente.cadera},{cliente.cuello},{cliente.tmb},{cliente.porcentaje_grasa},{cliente.peso_grasa},{cliente.masa_muscular},{cliente.agua_total}\n")
        messagebox.showinfo("Exportación", "Historial exportado con éxito a 'historial_clientes.csv'.")


class AdminApplication:
    pass


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Análisis de Composición Corporal")
        self.setup_ui()

    def setup_ui(self):
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(self.frame, text="Usuario:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username = tk.StringVar()
        ttk.Entry(self.frame, textvariable=self.username).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(self.frame, text="Contraseña:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.password = tk.StringVar()
        ttk.Entry(self.frame, textvariable=self.password, show='*').grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

        ttk.Button(self.frame, text="Iniciar Sesión", command=self.login).grid(row=2, column=0, pady=10)
        ttk.Button(self.frame, text="Registrarse", command=self.register).grid(row=2, column=1, pady=10)

    def login(self):
        username = self.username.get()
        password = self.password.get()

        session = Session()
        user = session.query(Usuario).filter_by(username=username).first()
        if user and user.check_password(password):
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
            self.root.withdraw()  # Oculta la ventana de login
            main_app_window = tk.Toplevel()
            MainApplication(main_app_window)
            main_app_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        session.close()

    def on_closing(self):
        self.root.destroy()  # Cierra la aplicación completamente

    def register(self):
        username = self.username.get()
        password = self.password.get()

        session = Session()
        existing_user = session.query(Usuario).filter_by(username=username).first()
        if existing_user:
            messagebox.showerror("Error", "El nombre de usuario ya existe")
        else:
            new_user = Usuario(username=username)
            new_user.set_password(password)
            session.add(new_user)
            session.commit()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente")
        session.close()

def main():
    root = tk.Tk()
    login_window = LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()

