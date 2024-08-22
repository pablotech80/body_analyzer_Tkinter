import math


def validar_entrada(valor, min_valor, max_valor, nombre):
    """Valida que el valor esté dentro del rango especificado."""
    if not min_valor <= valor <= max_valor:
        raise ValueError(f"{nombre} debe estar entre {min_valor} y {max_valor}")


def calcular_tmb(peso, altura, edad, genero):
    """
    Calcula la Tasa Metabólica Basal (TMB) usando la fórmula de Harris-Benedict.

    :param peso: Peso en kg
    :param altura: Altura en cm
    :param edad: Edad en años
    :param genero: 'h' para hombre, 'm' para mujer
    :return: TMB en kcal/día
    """
    validar_entrada(peso, 30, 300, "Peso")
    validar_entrada(altura, 100, 250, "Altura")
    validar_entrada(edad, 1, 120, "Edad")

    if genero.lower() not in ['h', 'm']:
        raise ValueError("Género debe ser 'h' o 'm'")

    if genero.lower() == 'h':
        return 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * edad)
    else:
        return 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * edad)


def calcular_imc(peso, altura):
    """
    Calcula el Índice de Masa Corporal (IMC).

    :param peso: Peso en kg
    :param altura: Altura en cm
    :return: IMC
    """
    validar_entrada(peso, 30, 300, "Peso")
    validar_entrada(altura, 100, 250, "Altura")

    return peso / ((altura / 100) ** 2)


def calcular_porcentaje_grasa(cintura, cadera, cuello, altura, genero):
    """
    Calcula el porcentaje de grasa corporal usando la fórmula de la Marina de EE.UU.

    :param cintura: Circunferencia de cintura en cm
    :param cadera: Circunferencia de cadera en cm
    :param cuello: Circunferencia de cuello en cm
    :param altura: Altura en cm
    :param genero: 'h' para hombre, 'm' para mujer
    :return: Porcentaje de grasa corporal
    """
    validar_entrada(cintura, 50, 200, "Cintura")
    validar_entrada(cadera, 50, 200, "Cadera")
    validar_entrada(cuello, 20, 60, "Cuello")
    validar_entrada(altura, 100, 250, "Altura")

    if genero.lower() not in ['h', 'm']:
        raise ValueError("Género debe ser 'h' o 'm'")

    try:
        if genero.lower() == 'h':
            porcentaje_grasa = 495 / (
                        1.0324 - 0.19077 * math.log10(cintura - cuello) + 0.15456 * math.log10(altura)) - 450
        else:
            porcentaje_grasa = 495 / (
                        1.29579 - 0.35004 * math.log10(cintura + cadera - cuello) + 0.22100 * math.log10(altura)) - 450
        return max(0, min(porcentaje_grasa, 100))  # Limita el resultado entre 0% y 100%
    except ValueError:
        raise ValueError("Error en los valores ingresados para el cálculo de grasa corporal.")


def calcular_masa_magra(peso, porcentaje_grasa):
    """
    Calcula la masa magra.

    :param peso: Peso en kg
    :param porcentaje_grasa: Porcentaje de grasa corporal
    :return: Masa magra en kg
    """
    return peso * (1 - porcentaje_grasa / 100)


def calcular_agua_corporal(peso, porcentaje_grasa, genero):
    """
    Estima el agua corporal total.

    :param peso: Peso en kg
    :param porcentaje_grasa: Porcentaje de grasa corporal
    :param genero: 'h' para hombre, 'm' para mujer
    :return: Agua corporal total en litros
    """
    if genero.lower() == 'h':
        return 2.447 - 0.09156 * porcentaje_grasa + 0.1074 * peso
    else:
        return -2.097 + 0.1069 * peso


def realizar_calculos(datos):
    """
    Realiza todos los cálculos y devuelve los resultados.

    :param datos: Diccionario con los datos del usuario
    :return: Diccionario con los resultados de los cálculos
    """
    try:
        peso = float(datos['peso'])
        altura = float(datos['altura'])
        edad = int(datos['edad'])
        genero = datos['genero'].lower()
        cintura = float(datos['cintura'])
        cadera = float(datos['cadera']) if genero == 'm' else 0
        cuello = float(datos['cuello'])

        tmb = calcular_tmb(peso, altura, edad, genero)
        imc = calcular_imc(peso, altura)
        porcentaje_grasa = calcular_porcentaje_grasa(cintura, cadera, cuello, altura, genero)
        masa_magra = calcular_masa_magra(peso, porcentaje_grasa)
        agua_corporal = calcular_agua_corporal(peso, porcentaje_grasa, genero)

        return {
            "tmb": round(tmb, 2),
            "imc": round(imc, 2),
            "porcentaje_grasa": round(porcentaje_grasa, 2),
            "masa_magra": round(masa_magra, 2),
            "agua_corporal": round(agua_corporal, 2)
        }
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Error inesperado: {str(e)}"}