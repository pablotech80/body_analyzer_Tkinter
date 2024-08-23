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

def actualizar_panel(event):
    """
    Actualiza los campos de la interfaz según el género seleccionado.
    """
    genero_val = genero.get().lower()
    if genero_val == 'h':
        cadera_label.grid_remove()
        cadera_entry.grid_remove()
    else:
        cadera_label.grid()
        cadera_entry.grid()

def actualizar_macros(event):
    """
    Actualiza los porcentajes de macronutrientes según el objetivo seleccionado.
    """
    objetivo_val = objetivo.get().lower()
    if objetivo_val == 'mantener':
        proteina.set("30")
        carbohidrato.set("40")
        grasa.set("30")
    elif objetivo_val == 'perder':
        proteina.set("40")
        carbohidrato.set("40")
        grasa.set("20")
    elif objetivo_val == 'ganar':
        proteina.set("30")
        carbohidrato.set("50")
        grasa.set("20")

def calcular():
    """
    Realiza los cálculos de TMB, IMC, porcentaje de grasa, peso de grasa, masa magra,
    agua total, FFMI y muestra los resultados en la interfaz.
    """
    if not validar_entradas():
        return

    peso_val = float(peso.get())
    altura_val = float(altura.get())
    edad_val = int(edad.get())
    genero_val = genero.get().lower()
    cintura_val = float(cintura.get())
    cadera_val = float(cadera.get()) if genero_val == 'm' else 0.0
    cuello_val = float(cuello.get())
    objetivo_val = objetivo.get().lower()

    # Calcular TMB
    tmb = round(calcular_tmb(peso_val, altura_val, edad_val, genero_val), 2)
    # Calcular IMC
    imc = round(calcular_imc(peso_val, altura_val), 2)
    # Calcular porcentaje de grasa corporal (Marina Estadounidense)
    porcentaje_grasa = round(calcular_porcentaje_grasa(cintura_val, cadera_val, cuello_val, altura_val, genero_val), 2)
    # Calcular peso de grasa corporal
    peso_grasa = round((porcentaje_grasa / 100) * peso_val, 2)
    # Calcular masa magra
    masa_magra = round(calcular_masa_magra(peso_val, porcentaje_grasa), 2)
    # Calcular FFMI
    ffmi = round(calcular_ffmi(masa_magra, altura_val), 2)
    # Interpretar FFMI
    interpretacion_ffmi_val = interpretar_ffmi(ffmi, genero_val)
    # Calcular agua total del cuerpo
    agua_total = round(calcular_agua_total(peso_val, altura_val, edad_val, genero_val), 2)
    # Interpretar IMC considerando el FFMI
    interpretacion = interpretar_imc(imc, ffmi, genero_val)
    # Calcular peso saludable
    peso_min, peso_max = calcular_peso_saludable(altura_val)
    peso_min = round(peso_min, 2)
    peso_max = round(peso_max, 2)
    # Calcular sobrepeso
    sobrepeso = round(max(0, peso_val - peso_max), 2)  # Si el peso está dentro del rango saludable, sobrepeso es 0
    # Calcular Relación Cintura/Cadera
    rcc = round(calcular_relacion_cintura_cadera(cintura_val, cadera_val) if genero_val == 'm' else 0.0, 2)
    interpretacion_rcc_val = interpretar_rcc(rcc, genero_val) if rcc != 0.0 else "N/A"
    # Calcular Ratio Cintura/Altura
    ratio_cintura_altura = round(calcular_ratio_cintura_altura(cintura_val, altura_val), 2)
    interpretacion_ratio_cintura_altura_val = interpretar_ratio_cintura_altura(ratio_cintura_altura)
    # Calcular Calorías Diarias Necesarias
    calorias_diarias = round(calcular_calorias_diarias(tmb, objetivo_val), 2)
    # Calcular Macronutrientes
    proteinas, carbohidratos, grasas = calcular_macronutrientes(calorias_diarias, objetivo_val)
    proteinas = round(proteinas, 2)
    carbohidratos = round(carbohidratos, 2)
    grasas = round(grasas, 2)
    # Interpretar porcentaje de grasa
    interpretacion_porcentaje_grasa = interpretar_porcentaje_grasa(porcentaje_grasa, genero_val)

    # Mostrar resultados en la misma ventana
    resultado_tmb.set(f"TMB: {tmb:.2f} kcal/día")
    resultado_imc.set(f"IMC: {imc:.2f}")
    resultado_porcentaje_grasa.set(f"Porcentaje de Grasa: {porcentaje_grasa:.2f}% ({interpretacion_porcentaje_grasa})")
    resultado_peso_grasa.set(f"Peso de Grasa Corporal: {peso_grasa:.2f} kg")
    resultado_masa_muscular.set(f"Masa Magra: {masa_magra:.2f} kg")
    resultado_agua_total.set(f"Agua Total del Cuerpo: {agua_total:.2f} litros")
    resultado_ffmi.set(f"FFMI: {ffmi:.2f}")
    interpretacion_ffmi.set(f"Interpretación FFMI: {interpretacion_ffmi_val}")
    interpretacion_imc.set(f"Interpretación IMC: {interpretacion}")
    resultado_peso_saludable.set(f"Peso Saludable: {peso_min:.2f} kg - {peso_max:.2f} kg")
    resultado_sobrepeso.set(f"Sobrepeso: {sobrepeso:.2f} kg")
    resultado_rcc.set(f"Relación Cintura/Cadera: {rcc} ({interpretacion_rcc_val})")
    resultado_ratio_cintura_altura.set(f"Ratio Cintura/Altura: {ratio_cintura_altura:.2f} ({interpretacion_ratio_cintura_altura_val})")
    resultado_calorias_diarias.set(f"Calorías Diarias Necesarias: {calorias_diarias:.2f} kcal")
    resultado_macronutrientes.set(f"Macronutrientes: Proteínas: {proteinas:.2f}g, Carbohidratos: {carbohidratos:.2f}g, Grasas: {grasas:.2f}g")

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

    resultado_salud.set(mensaje_salud)

def validar_entradas():
    """
    Valida que todas las entradas necesarias estén presentes y correctas.
    """
    try:
        float(peso.get())
        float(altura.get())
        int(edad.get())
        float(cintura.get())
        float(cuello.get())
        if genero.get().lower() == 'm':
            float(cadera.get())
    except ValueError:
        messagebox.showerror("Error de entrada", "Por favor, ingrese valores numéricos válidos.")
        return False
    return True

def guardar_perfil():
    """
    Guarda los datos del cliente en la base de datos.
    """
    if not validar_entradas():
        return

    nombre_val = nombre.get()
    fecha_val = datetime.now()
    peso_val = float(peso.get())
    altura_val = float(altura.get())
    edad_val = int(edad.get())
    genero_val = genero.get().lower()
    cintura_val = float(cintura.get())
    cadera_val = float(cadera.get()) if genero_val == 'm' else 0.0
    cuello_val = float(cuello.get())
    objetivo_val = objetivo.get().lower()

    # Calcular TMB
    tmb = round(calcular_tmb(peso_val, altura_val, edad_val, genero_val), 2)
    # Calcular IMC
    imc = round(calcular_imc(peso_val, altura_val), 2)
    # Calcular porcentaje de grasa corporal
    porcentaje_grasa = round(calcular_porcentaje_grasa(cintura_val, cadera_val, cuello_val, altura_val, genero_val), 2)
    # Calcular peso de grasa corporal
    peso_grasa = round((porcentaje_grasa / 100) * peso_val, 2)
    # Calcular masa magra
    masa_magra = round(calcular_masa_magra(peso_val, porcentaje_grasa), 2)
    # Calcular agua total del cuerpo
    agua_total = round(calcular_agua_total(peso_val, altura_val, edad_val, genero_val), 2)

    cliente_data = {
        'nombre': nombre_val,
        'fecha': fecha_val,
        'peso': peso_val,
        'altura': altura_val,
        'edad': edad_val,
        'genero': genero_val,
        'cintura': cintura_val,
        'cadera': cadera_val,
        'cuello': cuello_val,
        'tmb': tmb,
        'porcentaje_grasa': porcentaje_grasa,
        'peso_grasa': peso_grasa,
        'masa_muscular': masa_magra,
        'agua_total': agua_total
    }

    guardar_datos(cliente_data)
    messagebox.showinfo("Guardado", "Datos del cliente guardados con éxito.")

def limpiar_campos():
    """
    Limpia todos los campos de entrada y resultados.
    """
    nombre.set("")
    peso.set("")
    altura.set("")
    edad.set("")
    genero.set("")
    objetivo.set("")
    proteina.set("")
    carbohidrato.set("")
    grasa.set("")
    cadera.set("")
    cintura.set("")
    cuello.set("")
    resultado_tmb.set("")
    resultado_imc.set("")
    resultado_porcentaje_grasa.set("")
    resultado_peso_grasa.set("")
    resultado_masa_muscular.set("")
    resultado_agua_total.set("")
    resultado_ffmi.set("")
    interpretacion_ffmi.set("")
    interpretacion_imc.set("")
    resultado_peso_saludable.set("")
    resultado_sobrepeso.set("")
    resultado_rcc.set("")
    resultado_ratio_cintura_altura.set("")
    resultado_calorias_diarias.set("")
    resultado_macronutrientes.set("")
    resultado_salud.set("")

def mostrar_historial():
    """
    Muestra el historial de clientes guardados en la base de datos.
    """
    historial = recuperar_historial()
    historial_texto = "\n".join([f"{cliente.nombre} - {cliente.fecha}" for cliente in historial])
    messagebox.showinfo("Historial de Clientes", historial_texto)

def exportar_historial():
    """
    Exporta el historial de clientes guardados a un archivo CSV.
    """
    historial = recuperar_historial()
    with open('historial_clientes.csv', 'w') as file:
        file.write("Nombre,Fecha,Peso,Altura,Edad,Género,Cintura,Cadera,Cuello,TMB,Porcentaje Grasa,Peso Grasa,Masa Muscular,Agua Total\n")
        for cliente in historial:
            file.write(f"{cliente.nombre},{cliente.fecha},{cliente.peso},{cliente.altura},{cliente.edad},{cliente.genero},{cliente.cintura},{cliente.cadera},{cliente.cuello},{cliente.tmb},{cliente.porcentaje_grasa},{cliente.peso_grasa},{cliente.masa_muscular},{cliente.agua_total}\n")
    messagebox.showinfo("Exportación", "Historial exportado con éxito.")

# Crear la ventana principal
root = tk.Tk()
root.title("Análisis de Composición Corporal by CoachBodyFit")

# Agregar un ícono a la ventana
root.iconbitmap('/Users/user/developer_proyect/proyecto_bodyfit/pythonProject/calcu.ico')

# Crear estilos personalizados
style = ttk.Style()
style.configure('TButton', font=('Arial', 12, 'bold'))
style.configure('TLabel', font=('Arial', 12))
style.configure('TEntry', font=('Arial', 12))

# Crear el marco para la entrada de datos
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Crear el marco para los botones
button_frame = ttk.Frame(frame, padding="10")
button_frame.grid(row=29, column=0, columnspan=2, sticky=(tk.W, tk.E))

# Etiquetas y campos de entrada
ttk.Label(frame, text="Nombre Completo:", style="TLabel").grid(row=0, column=0, sticky=tk.W)
nombre = tk.StringVar()
ttk.Entry(frame, textvariable=nombre, style="TEntry").grid(row=0, column=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Peso (kg):", style="TLabel").grid(row=1, column=0, sticky=tk.W)
peso = tk.StringVar()
ttk.Entry(frame, textvariable=peso, style="TEntry").grid(row=1, column=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Altura (cm):", style="TLabel").grid(row=2, column=0, sticky=tk.W)
altura = tk.StringVar()
ttk.Entry(frame, textvariable=altura, style="TEntry").grid(row=2, column=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Edad:", style="TLabel").grid(row=3, column=0, sticky=tk.W)
edad = tk.StringVar()
ttk.Entry(frame, textvariable=edad, style="TEntry").grid(row=3, column=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Género (H/M):", style="TLabel").grid(row=4, column=0, sticky=tk.W)
genero = tk.StringVar()
genero_entry = ttk.Entry(frame, textvariable=genero, style="TEntry")
genero_entry.grid(row=4, column=1, sticky=(tk.W, tk.E))
genero_entry.bind('<KeyRelease>', actualizar_panel)

ttk.Label(frame, text="Objetivo (mantener/perder/ganar):", style="TLabel").grid(row=5, column=0, sticky=tk.W)
objetivo = tk.StringVar()
objetivo_entry = ttk.Entry(frame, textvariable=objetivo, style="TEntry")
objetivo_entry.grid(row=5, column=1, sticky=(tk.W, tk.E))
objetivo_entry.bind('<KeyRelease>', actualizar_macros)

ttk.Label(frame, text="Proteína (%):", style="TLabel").grid(row=6, column=0, sticky=tk.W)
proteina = tk.StringVar()
ttk.Entry(frame, textvariable=proteina, style="TEntry").grid(row=6, column=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Carbohidrato (%):", style="TLabel").grid(row=7, column=0, sticky=tk.W)
carbohidrato = tk.StringVar()
ttk.Entry(frame, textvariable=carbohidrato, style="TEntry").grid(row=7, column=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Grasa (%):", style="TLabel").grid(row=8, column=0, sticky=tk.W)
grasa = tk.StringVar()
ttk.Entry(frame, textvariable=grasa, style="TEntry").grid(row=8, column=1, sticky=(tk.W, tk.E))

cadera_label = ttk.Label(frame, text="Circunferencia de Cadera (cm):", style="TLabel")
cadera_label.grid(row=10, column=0, sticky=tk.W)
cadera = tk.StringVar()
cadera_entry = ttk.Entry(frame, textvariable=cadera, style="TEntry")
cadera_entry.grid(row=10, column=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Circunferencia de Cintura (cm):", style="TLabel").grid(row=9, column=0, sticky=tk.W)
cintura = tk.StringVar()
ttk.Entry(frame, textvariable=cintura, style="TEntry").grid(row=9, column=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Circunferencia de Cuello (cm):", style="TLabel").grid(row=11, column=0, sticky=tk.W)
cuello = tk.StringVar()
ttk.Entry(frame, textvariable=cuello, style="TEntry").grid(row=11, column=1, sticky=(tk.W, tk.E))

# Etiquetas para los resultados
ttk.Label(frame, text="Resultados:", style="TLabel").grid(row=12, column=0, sticky=tk.W)
resultado_tmb = tk.StringVar()
ttk.Label(frame, textvariable=resultado_tmb, style="TLabel").grid(row=13, column=0, columnspan=2, sticky=(tk.W, tk.E))

resultado_imc = tk.StringVar()
ttk.Label(frame, textvariable=resultado_imc, style="TLabel").grid(row=14, column=0, columnspan=2, sticky=(tk.W, tk.E))

resultado_porcentaje_grasa = tk.StringVar()
ttk.Label(frame, textvariable=resultado_porcentaje_grasa, style="TLabel").grid(row=15, column=0, columnspan=2, sticky=(tk.W, tk.E))

resultado_peso_grasa = tk.StringVar()
ttk.Label(frame, textvariable=resultado_peso_grasa, style="TLabel").grid(row=16, column=0, columnspan=2, sticky=(tk.W, tk.E))

resultado_masa_muscular = tk.StringVar()
ttk.Label(frame, textvariable=resultado_masa_muscular, style="TLabel").grid(row=17, column=0, columnspan=2, sticky=(tk.W, tk.E))

resultado_agua_total = tk.StringVar()
ttk.Label(frame, textvariable=resultado_agua_total, style="TLabel").grid(row=18, column=0, columnspan=2, sticky=(tk.W, tk.E))

resultado_ffmi = tk.StringVar()
ttk.Label(frame, textvariable=resultado_ffmi, style="TLabel").grid(row=19, column=0, columnspan=2, sticky=(tk.W, tk.E))

interpretacion_ffmi = tk.StringVar()
ttk.Label(frame, textvariable=interpretacion_ffmi, style="TLabel").grid(row=20, column=0, columnspan=2, sticky=(tk.W, tk.E))

interpretacion_imc = tk.StringVar()
ttk.Label(frame, textvariable=interpretacion_imc, style="TLabel").grid(row=21, column=0, columnspan=2, sticky=(tk.W, tk.E))

resultado_peso_saludable = tk.StringVar()
ttk.Label(frame, textvariable=resultado_peso_saludable, style="TLabel").grid(row=22, column=0, columnspan=2, sticky=(tk.W, tk.E))

resultado_sobrepeso = tk.StringVar()
ttk.Label(frame, textvariable=resultado_sobrepeso, style="TLabel").grid(row=23, column=0, columnspan=2, sticky=(tk.W, tk.E))

resultado_rcc = tk.StringVar()
ttk.Label(frame, textvariable=resultado_rcc, style="TLabel").grid(row=24, column=0, columnspan=2, sticky=(tk.W, tk.E))

resultado_ratio_cintura_altura = tk.StringVar()
ttk.Label(frame, textvariable=resultado_ratio_cintura_altura, style="TLabel").grid(row=25, column=0, columnspan=2, sticky=(tk.W, tk.E))

resultado_calorias_diarias = tk.StringVar()
ttk.Label(frame, textvariable=resultado_calorias_diarias, style="TLabel").grid(row=26, column=0, columnspan=2, sticky=(tk.W, tk.E))

resultado_macronutrientes = tk.StringVar()
ttk.Label(frame, textvariable=resultado_macronutrientes, style="TLabel").grid(row=27, column=0, columnspan=2, sticky=(tk.W, tk.E))

resultado_salud = tk.StringVar()
ttk.Label(frame, textvariable=resultado_salud, wraplength=400, style="TLabel").grid(row=28, column=0, columnspan=2, sticky=(tk.W, tk.E))

# Botones para calcular, guardar, limpiar, exportar y ver historial
ttk.Button(button_frame, text="Calcular", command=calcular, style="TButton").grid(row=0, column=0, sticky=(tk.W, tk.E))
ttk.Button(button_frame, text="Guardar", command=guardar_perfil, style="TButton").grid(row=0, column=1, sticky=(tk.W, tk.E))
ttk.Button(button_frame, text="Limpiar", command=limpiar_campos, style="TButton").grid(row=1, column=0, sticky=(tk.W, tk.E))
ttk.Button(button_frame, text="Historial", command=mostrar_historial, style="TButton").grid(row=1, column=1, sticky=(tk.W, tk.E))
ttk.Button(button_frame, text="Exportar", command=exportar_historial, style="TButton").grid(row=1, column=2, sticky=(tk.W, tk.E))

# Iniciar el bucle de eventos de Tkinter
root.mainloop()

