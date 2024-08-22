import math


def calcular_tmb(peso, altura, edad, genero):
    # Cálculo de la Tasa Metabólica Basal (TMB)
    if genero == 'h':
        return 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * edad)
    else:
        return 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * edad)


def calcular_imc(peso, altura):
    # Cálculo del Índice de Masa Corporal (IMC)
    return peso / (altura / 100) ** 2


def calcular_porcentaje_grasa(cintura, cadera, cuello, altura, genero):
    try:
        if genero == 'h':
            porcentaje_grasa = 495 / (
                        1.0324 - 0.19077 * math.log10(cintura - cuello) + 0.15456 * math.log10(altura)) - 450
        else:
            porcentaje_grasa = 495 / (
                        1.29579 - 0.35004 * math.log10(cintura + cadera - cuello) + 0.22100 * math.log10(altura)) - 450
        return float(porcentaje_grasa)
    except ValueError:
        print("Error en los valores ingresados para el cálculo de grasa corporal.")
        return None


# Esta función realiza todos los cálculos y devuelve los resultados
def realizar_calculos(peso, altura, edad, genero, cintura, cadera, cuello):
    tmb = calcular_tmb(peso, altura, edad, genero)
    imc = calcular_imc(peso, altura)
    grasa = calcular_porcentaje_grasa(cintura, cadera, cuello, altura, genero)

    return {
        "tmb": tmb,
        "imc": imc,
        "grasa": grasa
    }
