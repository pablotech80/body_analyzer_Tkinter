from datetime import datetime

import math
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Cliente, Base

# Configuración de la base de datos
engine = create_engine('sqlite:///clientes.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def calcular_tmb(peso, altura, edad, genero):
    """
    Calcula la Tasa Metabólica Basal (TMB) usando la fórmula de Harris-Benedict.
    """
    if genero == 'h':
        tmb = 88.362 + (13.397 * peso) + (4.799 * altura) - (5.677 * edad)
    else:
        tmb = 447.593 + (9.247 * peso) + (3.098 * altura) - (4.330 * edad)
    return tmb

def calcular_imc(peso, altura):
    """
    Calcula el Índice de Masa Corporal (IMC).
    """
    altura_m = altura / 100
    imc = peso / (altura_m ** 2)
    return imc

def calcular_porcentaje_grasa(cintura, cadera, cuello, altura, genero):
    """
    Calcula el porcentaje de grasa corporal usando la fórmula de la Marina Estadounidense.
    """
    if genero == 'h':
        porcentaje_grasa = 495 / (1.0324 - 0.19077 * math.log10(cintura - cuello) + 0.15456 * math.log10(altura)) - 450
    else:
        porcentaje_grasa = 495 / (1.29579 - 0.35004 * math.log10(cintura + cadera - cuello) + 0.22100 * math.log10(altura)) - 450
    return porcentaje_grasa

def calcular_agua_total(peso, altura, edad, genero):
    """
    Calcula el agua total del cuerpo usando una fórmula simplificada.
    """
    if genero == 'h':
        agua_total = 2.447 - (0.09156 * edad) + (0.1074 * altura) + (0.3362 * peso)
    else:
        agua_total = -2.097 + (0.1069 * altura) + (0.2466 * peso)
    return agua_total

def interpretar_imc(imc, ffmi, genero):
    """
    Interpreta el resultado del IMC considerando el FFMI.
    """
    if imc > 25 and ffmi > 19 if genero == 'm' else ffmi > 16:
        return "El IMC es alto, pero puede estar influenciado por una alta masa muscular."
    elif imc < 18.5:
        return "El IMC es bajo, se recomienda consultar con un profesional de salud."
    else:
        return "El IMC está dentro del rango normal."

def calcular_peso_saludable(altura):
    """
    Calcula el rango de peso saludable en base al IMC.
    """
    altura_m = altura / 100
    peso_min = 18.5 * (altura_m ** 2)
    peso_max = 24.9 * (altura_m ** 2)
    return peso_min, peso_max

def calcular_masa_magra(peso, porcentaje_grasa):
    """
    Calcula la masa magra del cuerpo.
    """
    masa_magra = peso * ((100 - porcentaje_grasa) / 100)
    return masa_magra

def calcular_ffmi(masa_magra, altura):
    """
    Calcula el índice de masa libre de grasa (FFMI).
    """
    altura_m = altura / 100
    ffmi = masa_magra / (altura_m ** 2)
    return ffmi

def interpretar_ffmi(ffmi, genero):
    """
    Interpreta el resultado del FFMI.
    """
    if genero == 'h':
        if ffmi < 18:
            return "Lejos del máximo potencial (pobre forma física)"
        elif 18 <= ffmi < 19:
            return "Cercano a la normalidad"
        elif 19 <= ffmi < 20:
            return "Normal"
        elif 20 <= ffmi < 21:
            return "Superior a la normalidad (buena forma física)"
        elif 21 <= ffmi < 22.5:
            return "Fuerte (Muy buena forma física)"
        elif 22.5 <= ffmi < 24:
            return "Muy fuerte (Excelente forma física). Cerca del máximo potencial."
        elif 24 <= ffmi < 25.5:
            return "Muy cerca del máximo potencial."
        elif 25.5 <= ffmi < 27:
            return "Potencial máximo natural alcanzado. Muy muy pocos llegan naturales"
        elif 27 <= ffmi < 29:
            return "Prácticamente imposible sin fármacos"
        else:
            return "Imposible sin fármacos"
    else:
        if ffmi < 13.5:
            return "Lejos del máximo potencial (pobre forma física)"
        elif 13.5 <= ffmi < 14.5:
            return "Cercano a la normalidad"
        elif 14.5 <= ffmi < 16:
            return "Normal"
        elif 16 <= ffmi < 17:
            return "Superior a la normalidad (buena forma física)"
        elif 17 <= ffmi < 18.5:
            return "Fuerte (Muy buena forma física)"
        elif 18.5 <= ffmi < 20:
            return "Muy fuerte (Excelente forma física). Cerca del máximo potencial."
        elif 20 <= ffmi < 21:
            return "Muy cerca del máximo potencial."
        elif 21 <= ffmi < 22:
            return "Potencial máximo natural alcanzado. Muy muy pocos llegan naturales"
        elif 22 <= ffmi < 23:
            return "Prácticamente imposible sin fármacos"
        else:
            return "Imposible sin fármacos"

def calcular_relacion_cintura_cadera(cintura, cadera):
    """
    Calcula la relación cintura/cadera.
    """
    return cintura / cadera

def interpretar_rcc(rcc, genero):
    """
    Interpreta la relación cintura/cadera.
    """
    if genero == 'h':
        if rcc > 0.95:
            return "Alto riesgo"
        elif 0.90 < rcc <= 0.95:
            return "Moderado riesgo"
        else:
            return "Bajo riesgo"
    else:
        if rcc > 0.85:
            return "Alto riesgo"
        elif 0.80 < rcc <= 0.85:
            return "Moderado riesgo"
        else:
            return "Bajo riesgo"

def calcular_ratio_cintura_altura(cintura, altura):
    """
    Calcula el ratio cintura/altura.
    """
    return cintura / altura

def interpretar_ratio_cintura_altura(ratio):
    """
    Interpreta el ratio cintura/altura.
    """
    if ratio >= 0.6:
        return "Alto riesgo"
    elif 0.5 <= ratio < 0.6:
        return "Moderado riesgo"
    else:
        return "Bajo riesgo"

def calcular_calorias_diarias(tmb, objetivo):
    """
    Calcula las calorías diarias necesarias según el objetivo.
    """
    if objetivo == 'mantener':
        return tmb * 1.2  # Factor de actividad moderado
    elif objetivo == 'perder':
        return tmb * 1.2 * 0.8  # 20% de reducción calórica
    elif objetivo == 'ganar':
        return tmb * 1.2 * 1.2  # 20% de aumento calórico

def calcular_macronutrientes(calorias, objetivo):
    """
    Calcula los macronutrientes en gramos según el objetivo.
    """
    if objetivo == 'mantener':
        proteinas = (calorias * 0.30) / 4
        carbohidratos = (calorias * 0.40) / 4
        grasas = (calorias * 0.30) / 9
    elif objetivo == 'perder':
        proteinas = (calorias * 0.40) / 4
        carbohidratos = (calorias * 0.40) / 4
        grasas = (calorias * 0.20) / 9
    elif objetivo == 'ganar':
        proteinas = (calorias * 0.30) / 4
        carbohidratos = (calorias * 0.50) / 4
        grasas = (calorias * 0.20) / 9
    return float(proteinas), float(carbohidratos), float(grasas)


def interpretar_porcentaje_grasa(porcentaje_grasa, genero):
    """
    Interpreta el porcentaje de grasa corporal.
    """
    if genero == 'h':
        if porcentaje_grasa > 25:
            return "Alto"
        elif porcentaje_grasa < 6:
            return "Bajo"
        else:
            return "Normal"
    else:
        if porcentaje_grasa > 32:
            return "Alto"
        elif porcentaje_grasa < 16:
            return "Bajo"
        else:
            return "Normal"

def guardar_datos(cliente_data):
    """
    Guarda los datos del cliente en la base de datos.
    """
    cliente = Cliente(
        nombre=cliente_data['nombre'],
        fecha=cliente_data['fecha'],
        peso=cliente_data['peso'],
        altura=cliente_data['altura'],
        edad=cliente_data['edad'],
        genero=cliente_data['genero'],
        cintura=cliente_data['cintura'],
        cadera=cliente_data['cadera'],
        cuello=cliente_data['cuello'],
        tmb=cliente_data['tmb'],
        porcentaje_grasa=cliente_data['porcentaje_grasa'],
        peso_grasa=cliente_data['peso_grasa'],
        masa_muscular=cliente_data['masa_muscular'],
        agua_total=cliente_data['agua_total']
    )
    session.add(cliente)
    session.commit()

def recuperar_historial():
    """
    Recupera el historial de clientes de la base de datos.
    """
    return session.query(Cliente).all()
