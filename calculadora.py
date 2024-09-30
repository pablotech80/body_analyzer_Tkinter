import math, logging


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from typing import Union, Tuple, Dict, List


from constantes import (
    VALOR_TMB_HOMBRE, FACTOR_PESO_HOMBRE, FACTOR_ALTURA_HOMBRE, FACTOR_EDAD_HOMBRE,
    VALOR_TMB_MUJER, FACTOR_PESO_MUJER, FACTOR_ALTURA_MUJER, FACTOR_EDAD_MUJER,
    HOMBRE_ALTO_THRESHOLD, HOMBRE_BAJO_THRESHOLD,
    MUJER_ALTO_THRESHOLD, MUJER_BAJO_THRESHOLD,
    AGUA_TOTAL_HOMBRE_BASE, AGUA_TOTAL_HOMBRE_EDAD,
    AGUA_TOTAL_HOMBRE_ALTURA, AGUA_TOTAL_HOMBRE_PESO,
    AGUA_TOTAL_MUJER_BASE, AGUA_TOTAL_MUJER_ALTURA, AGUA_TOTAL_MUJER_PESO,
    IMC_MIN_SALUDABLE, IMC_MAX_SALUDABLE, IMC_SOBREPESO,
    IMC_OBESIDAD_1, IMC_OBESIDAD_2, IMC_OB_MORBIDA,
    IMC_MIN_SALUDABLE, IMC_MAX_SALUDABLE,
    FFMI_THRESHOLDS_HOMBRES, FFMI_THRESHOLDS_MUJERES,
    UMBRAL_RIESGO_ALTO_HOMBRE, UMBRAL_RIESGO_MODERADO_HOMBRE,
    UMBRAL_RIESGO_ALTO_MUJER, UMBRAL_RIESGO_MODERADO_MUJER

)
from models import Cliente, Base

'''Configuración de la base de datos'''

engine = create_engine('sqlite:///clientes.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def calcular_tmb(peso: Union[int, float], altura: Union[int, float], edad:[int ], genero: [str]):

    """Calcula la Tasa Metabólica Basal (TMB) usando la fórmula de Harris-Benedict.

        Args:
            peso (float): Peso del usuario en kilogramos.
            altura (float): Altura del usuario en centímetros.
            edad (int): Edad del usuario en años.
            genero (str): Género del usuario ('h' para hombre, 'm' para mujer).

        Returns:
            float: La TMB calculada
        """
    if genero == 'h':
            tmb = VALOR_TMB_HOMBRE + (FACTOR_PESO_HOMBRE * peso) + (FACTOR_ALTURA_HOMBRE * altura) - (FACTOR_EDAD_HOMBRE * edad)
    else:
            tmb = VALOR_TMB_MUJER + (FACTOR_PESO_MUJER * peso) + (FACTOR_ALTURA_MUJER * altura) - (FACTOR_EDAD_MUJER * edad)
    return tmb


def calcular_imc(peso: Union[int, float], altura: Union[int, float]) -> float:
    """
    Calcula el IMC en una categoría basada en los rangos de IMC definidos.

    Args:
        imc (float): El índice de masa corporal (IMC) calculado.

    Returns:
        str: La categoría correspondiente al IMC (e.g., "Peso saludable", "Sobrepeso").

    Raises:
        ValueError: Si el IMC es un valor inválido.
        @param peso:

    """

    # Validación del IMC
    if not isinstance(peso, (int, float)) or peso <= 0:
        raise ValueError("El Peso debe ser un número mayor que 0.")

    if not isinstance(altura, (int, float)) or altura <= 0:
        raise ValueError("La Altura debe ser un número mayor que 0. ")

    # calculo de IMC
    altura_m = altura / 100
    imc = peso / (altura_m ** 2)
    return imc

def clasificar_imc(imc: float) -> str:
    """
    Clasifica el IMC en diferentes categorías de salud.

    Args:
        imc (float): El índice de masa corporal (IMC) calculado.

    Returns:
        str: La categoría correspondiente al IMC (e.g., "Peso saludable", "Sobrepeso").
    """

    # Clasificación del IMC basado en los rangos
    if imc < IMC_MIN_SALUDABLE:
        return "Bajo peso"
    elif IMC_MIN_SALUDABLE <= imc <= IMC_MAX_SALUDABLE:
        return "Peso saludable"
    elif IMC_MAX_SALUDABLE < imc <= IMC_SOBREPESO:
        return "Sobrepeso"
    elif IMC_SOBREPESO < imc <= IMC_OBESIDAD_1:
        return "Obesidad grado 1"
    elif IMC_OBESIDAD_1 < imc <= IMC_OBESIDAD_2:
        return "Obesidad grado 2"
    elif IMC_OBESIDAD_2 < imc <= IMC_OB_MORBIDA:
        return "Obesidad mórbida"
    else:
        return "Obesidad extrema"

def interpretar_imc(imc: Union[int, float], ffmi: Union[int, float], genero: str) -> str:
    """
    Interpreta el resultado del IMC considerando el FFMI y el género.

    Args:
        imc (int | float): Índice de Masa Corporal calculado.
        ffmi (int | float): Índice de Masa Libre de Grasa (FFMI).
        genero (str): Género del usuario ('h' para hombre, 'm' para mujer).

    Returns:
        str: Interpretación del IMC basada en los valores de FFMI y género.

    Raises:
        ValueError: Si los valores de entrada no son válidos.
    """

    # Validación para IMC y FFMI
    if not isinstance(imc, (int, float)):
        raise ValueError("El IMC debe ser un número.")
    if not isinstance(ffmi, (int, float)):
        raise ValueError("El FFMI debe ser un número.")

    # Validación para el género
    if genero not in ['h', 'm']:
        raise ValueError("El género debe ser 'h' para hombres o 'm' para mujeres.")

    # Interpretación del IMC considerando el FFMI
    if genero == 'm':  # Para mujeres
        if imc > 25 and ffmi > 19:
            return "El IMC es alto, pero puede estar influenciado por una alta masa muscular."
    else:  # Para hombres
        if imc > 25 and ffmi > 16:
            return "El IMC es alto, pero puede estar influenciado por una alta masa muscular."

    if imc < 18.5:
        return "El IMC es bajo, lo que puede indicar bajo peso."
    else:
        return "El IMC está dentro del rango normal."


def calcular_porcentaje_grasa_hombre(peso: float, altura: Union[int, float],
                                     cintura: Union[int, float], cuello: Union[int, float]) -> float:

    """Calcula el porcentaje de grasa corporal para hombres."""

    # Validaciones
    for x in [peso, altura, cintura, cuello]:
        if not isinstance(x, (int, float)):
            raise ValueError("Todos los valores deben ser numéricos.")
    if any(x <= 0 for x in [peso, altura, cintura, cuello]):
        raise ValueError("Todos los valores deben ser mayores que 0.")

    # Fórmula corregida para calcular el porcentaje de grasa en hombres
    grasa_hombre = 495 / (1.0324 - 0.19077 * math.log10(cintura - cuello) + 0.15456 * math.log10(altura)) - 450

    # Validación del rango del porcentaje de grasa
    if grasa_hombre < 0 or grasa_hombre > 100:
        raise ValueError(
            f"El porcentaje de grasa calculado es inválido: {grasa_hombre:.2f}. Verifica las medidas ingresadas.")

    return grasa_hombre


def calcular_porcentaje_grasa_mujer(peso: Union[int, float], altura: Union[int, float], cintura: Union[int, float],
                                    cuello: Union[int, float], cadera: Union[int, float]) -> float:
    """Calcula el porcentaje de grasa corporal para mujeres."""
    # Validaciones
    if not all(isinstance(x, (int, float)) for x in [peso, altura, cintura, cuello, cadera]):
        raise ValueError("Todos los valores deben ser numéricos.")
    if any(x <= 0 for x in [peso, altura, cintura, cuello, cadera]):
        raise ValueError("Todos los valores deben ser mayores que 0.")

    # Fórmula corregida para calcular el porcentaje de grasa corporal en mujeres
    grasa_mujer = 495 / (1.29579 - 0.35004 * math.log10(cintura + cadera - cuello) + 0.22100 * math.log10(altura)) - 450

    # Validación del rango del porcentaje de grasa
    if grasa_mujer < 0 or grasa_mujer > 100:
        raise ValueError(
            f"El porcentaje de grasa calculado es inválido: {grasa_mujer:.2f}. Verifica las medidas ingresadas.")

    return grasa_mujer


def calcular_porcentaje_grasa(genero: str, peso: Union[int, float], altura: Union[int, float],
                              cintura: Union[int, float], cuello: Union[int, float],
                              cadera: Union[int, float] = None) -> float:
    """Calcula el porcentaje de grasa corporal según el género.

    Args:
        genero (str): 'h' para hombre, 'm' para mujer.
        peso (int | float): Peso en kilogramos.
        altura (int | float): Altura en centímetros.
        cintura (int | float): Circunferencia de la cintura en centímetros.
        cuello (int | float): Circunferencia del cuello en centímetros.
        cadera (int | float, opcional): Circunferencia de la cadera en centímetros (solo para mujeres).

    Returns:
        float: Porcentaje de grasa corporal.

    Raises:
        ValueError: Si los valores de entrada no son válidos o el género no es correcto.
    """

    # validación de género
    if genero not in ['h', 'm']:
        raise ValueError("El género debe ser 'h' para hombre o 'm' para mujer.")

    # cálculo según el género
    if genero == 'h':
        # No se necesita 'cadera' para hombres
        return calcular_porcentaje_grasa_hombre(peso, altura, cintura, cuello)
    elif genero == 'm':
        # Validar que cadera no sea None para mujeres
        if cadera is None:
            raise ValueError("La cadera es obligatoria para calcular el porcentaje de grasa en mujeres.")
        return calcular_porcentaje_grasa_mujer(peso, altura, cintura, cuello, cadera)


def interpretar_porcentaje_grasa(porcentaje_grasa: Union[int, float], genero: str) -> str:

    """
        Interpreta el porcentaje de grasa corporal basándose en el género y proporciona una evaluación cualitativa.

        Args:
            porcentaje_grasa (int | float): El porcentaje de grasa corporal calculado.
            genero (str): El género del individuo ('h' para hombres, 'm' para mujeres).

        Returns:
            str: Una cadena de texto que describe el estado del porcentaje de grasa corporal en términos de salud.

        Raises:
            ValueError: Si el porcentaje de grasa o el género no son válidos.
        """
# validaciones de entrada

    if not isinstance(porcentaje_grasa, (int, float)):
        raise ValueError("El porcentaje de grasa debe ser un número.")

    if porcentaje_grasa < 0 or porcentaje_grasa > 100:
        raise ValueError("El porcentaje de grasa debe estar entre 0 y 100.")

    if genero not in ['h', 'm']:
        raise ValueError("El género debe ser 'h' para hombre o 'm' para mujer.")

# interpretación según el género

    if genero == 'h':
        return interpretar_porcentaje_generico(porcentaje_grasa, HOMBRE_BAJO_THRESHOLD, HOMBRE_ALTO_THRESHOLD)
    elif genero == 'm':
        return interpretar_porcentaje_generico(porcentaje_grasa, MUJER_BAJO_THRESHOLD, MUJER_ALTO_THRESHOLD)

def interpretar_porcentaje_generico(porcentaje_grasa: float, bajo_threshold: float, alto_threshold: float) -> str:
    """
    Interpreta el porcentaje de grasa corporal usando thresholds específicos.

    Args:
        porcentaje_grasa (float): El porcentaje de grasa corporal calculado.
        bajo_threshold (float): Umbral inferior para definir si el porcentaje es bajo.
        alto_threshold (float): Umbral superior para definir si el porcentaje es alto.

    Returns:
        str: Evaluación cualitativa del porcentaje de grasa corporal.
    """
    if porcentaje_grasa > alto_threshold:
        return "Alto"
    elif porcentaje_grasa < bajo_threshold:
        return "Bajo"
    else:
        return "Normal"


def calcular_agua_total(peso: Union[int, float], altura: Union[int, float], edad: int, genero: str) -> float:
    """
    Calcula el agua total del cuerpo usando una fórmula simplificada.

    Args:
        peso (int | float): Peso del usuario en kilogramos.
        altura (int | float): Altura del usuario en centímetros.
        edad (int): Edad del usuario en años.
        genero (str): Género del usuario ('h' para hombre, 'm' para mujer).

    Returns:
        float: El total de agua en el cuerpo calculado en litros.

    Raises:
        ValueError: Si los datos de entrada no son válidos.
    """
    # Validación de entrada
    if not isinstance(peso, (int, float)) or peso <= 0:
        raise ValueError("El peso debe ser un número mayor que 0.")
    if not isinstance(altura, (int, float)) or altura <= 0:
        raise ValueError("La altura debe ser un número mayor que 0.")
    if not isinstance(edad, int) or edad <= 0:
        raise ValueError("La edad debe ser un número mayor que 0.")
    if genero not in ['h', 'm']:
        raise ValueError("El género debe ser 'h' para hombre o 'm' para mujer.")

    # Calcular el agua total según el género
    if genero == 'h':
        agua_total = AGUA_TOTAL_HOMBRE_BASE - (AGUA_TOTAL_HOMBRE_EDAD * edad) + (AGUA_TOTAL_HOMBRE_ALTURA * altura) + (
                AGUA_TOTAL_HOMBRE_PESO * peso)
    else:
        agua_total = AGUA_TOTAL_MUJER_BASE + (AGUA_TOTAL_MUJER_ALTURA * altura) + (AGUA_TOTAL_MUJER_PESO * peso)

    return agua_total  # Mueve el return fuera del bloque condicional para ambos casos


def calcular_peso_saludable(altura: float) -> Tuple[float, float]:

    """
        Calcula el rango de peso saludable basado en la altura utilizando el rango de IMC saludable.

        Args:
            altura (float): Altura del usuario en centímetros.

        Returns:
            tuple: Peso mínimo y máximo dentro del rango de IMC saludable en kilogramos.

        Raises:
            ValueError: Si la altura no es un número positivo.
        """
# validación de altura
    if not isinstance(altura, (int, float)) or altura <= 0:
        raise ValueError("La altura debe ser un número mayor a 0.")

# convertir altura a metros
    altura_m = altura / 100

# calcular peso min, max basados en el imc
    peso_min = IMC_MIN_SALUDABLE * (altura_m ** 2)
    peso_max = IMC_MAX_SALUDABLE * (altura_m ** 2)

    return peso_min, peso_max


def calcular_peso_min(altura: float) -> float:
    """
        Calcula el peso mínimo saludable basado en la altura y el IMC mínimo saludable.

        Args:
            altura (float): Altura del usuario en centímetros.

        Returns:
            float: Peso mínimo saludable en kilogramos.

        Raises:
            ValueError: Si la altura no es válida.
        """
# validación de la altura

    if not isinstance(altura, (int, float)) or altura <= 0:
        raise ValueError("La altura debe ser un número positivo.")

# convertir la altura en número positivo

    altura_m = altura /100

# calcular el peso min

    peso_min = IMC_MIN_SALUDABLE * (altura_m ** 2)
    return peso_min



def calcular_peso_max(altura: Union[int, float]) -> float:
    """
    Calcula el peso máximo saludable basado en la altura y el IMC máximo saludable.

    Args:
        altura (int | float): Altura del usuario en centímetros.

    Returns:
        float: Peso máximo saludable en kilogramos.

    Raises:
        ValueError: Si la altura no es válida.
        """

# validación de la altura
    if not isinstance(altura, (int, float)) or altura <= 0:
        raise ValueError("La altura debe ser un número positivo.")

# convertir la altura en número positivo

    altura_m = altura /100

# calcular el peso máximo saludable basado en el IMC máximo saludable

    peso_max = IMC_MAX_SALUDABLE * (altura_m ** 2)

    return peso_max



def calcular_sobrepeso(peso: Union[int, float], altura: Union[int, float]):

    """
    Calcula el sobrepeso comparando el peso actual con el peso máximo saludable.

    Args:
        peso (int | float): Peso actual del usuario en kilogramos.
        altura (int | float): Altura del usuario en centímetros.

    Returns:
        float: Sobrepeso calculado en kilogramos. Si no hay sobrepeso, devuelve 0.

    Raises:
        ValueError: Si el peso o la altura no son válidos.
        """


# validación de peso
    if not isinstance(peso, (int, float)) or peso <= 0:
        raise ValueError("El peso debe ser un número mayor que 0.")

    if not isinstance(altura, (int, float)) or altura <= 0:
        raise ValueError("La altura debe ser un número mayor que 0.")
# calcular el peso max saludable
    peso_max = calcular_peso_max(altura)

# calcular el sobrepeso. Si el peso es menor o igual al peso máximo, devuelve 0.
    sobrepeso = max(0, peso - peso_max)

    return sobrepeso

def calcular_masa_muscular(peso: Union[int, float], porcentaje_grasa: Union[int, float]) -> float:
    """
        Calcula la masa muscular (masa magra) del cuerpo descontando el porcentaje de grasa.

        Args:
            peso (int | float): Peso total del usuario en kilogramos.
            porcentaje_grasa (int | float): Porcentaje de grasa corporal del usuario.

        Returns:
            float: Masa muscular calculada en kilogramos.

        Raises:
            ValueError: Si el peso o el porcentaje de grasa no son válidos.
        """
# validaciones peso y porcentaje de grasa

    if not isinstance(peso, (int, float)) or peso <= 0:
        raise ValueError("El peso debe ser un número positivo")

    if not isinstance(porcentaje_grasa, (int, float)) or porcentaje_grasa < 0 or porcentaje_grasa >100:
        raise ValueError("El porcentaje de grasa debe ser un número entre 0 y 100.")

# calcular masa muscular
    masa_muscular = peso * ((100 - porcentaje_grasa) / 100)

    return masa_muscular


def calcular_ffmi(masa_muscular: Union[int, float], altura: Union[int, float]) -> float:
    """
        Calcula el Índice de Masa Libre de Grasa (FFMI).

        Args:
            masa_muscular (int | float): Masa muscular del usuario en kilogramos.
            altura (int | float): Altura del usuario en centímetros.

        Returns:
            float: El FFMI calculado basado en la masa muscular y la altura.

        Raises:
            ValueError: Si la masa muscular o la altura no son válidos.
        """
# validaciones de altura y masa muscular

    if not isinstance(masa_muscular, (int, float)) or masa_muscular <= 0:
        raise ValueError("La masa muscular debe ser un número positivo.")

    if not isinstance(altura, (int, float)) or altura <= 0:
        raise ValueError("La altura debe ser un número mayor que 0.")

# convertir altura a metros
    altura_m = altura / 100

# calcular ffmi
    ffmi = masa_muscular / (altura_m ** 2)
    return ffmi


def interpretar_ffmi_genero(ffmi, thresholds):
    for threshold, description in thresholds:
        if ffmi < threshold:
            return description
    return "Imposible sin fármacos"

def interpretar_ffmi(ffmi: float, genero: str) -> str:
    """
        Proporciona una interpretación del FFMI basado en rangos preestablecidos que varían según el género.

        Args:
            ffmi (float): Valor del FFMI a interpretar.
            genero (str): Género del usuario ('h' para hombres, 'm' para mujeres).

        Returns:
            str: Descripción del nivel de forma física basado en el FFMI.
        """
    if genero == 'h':
        return interpretar_ffmi_genero(ffmi, FFMI_THRESHOLDS_HOMBRES)
    elif genero == 'm':
        return interpretar_ffmi_genero(ffmi, FFMI_THRESHOLDS_MUJERES)
    else:
        return "Género no válido"



def calcular_rcc(cintura: Union[int, float], cadera: Union[int, float]) -> float:
    """
        Calcula la relación cintura-cadera, un indicador de distribución de grasa corporal en la zona abdominal.

        Args:
            cintura (int | float): Medida de la cintura en centímetros.
            cadera (int | float): Medida de la cadera en centímetros.

        Returns:
            float: Relación cintura-cadera calculada.

        Raises:
            ValueError: Si la cintura o la cadera no son válidas.
        """

# validaciones cintura, cadera
    if not isinstance(cintura, (int, float)) or cintura <= 0:
        raise ValueError("La cintura debe ser un número positivo.")

    if not isinstance(cadera, (int, float)) or cadera <= 0:
        raise ValueError("La cadera debe ser un número positivo y mayor que 0.")

# calcular la relación cintura-cadera

    rcc = cintura / cadera
    return rcc

def interpretar_rcc(rcc: Union[int, float], genero: str) -> str:
    """
    Interpreta la relación cintura-cadera basándose en umbrales específicos de riesgo según el género.

    Args:
        rcc (int | float): Relación cintura-cadera calculada.
        genero (str): Género del usuario ('h' para hombre, 'm' para mujer).

    Returns:
        str: Interpretación del nivel de riesgo asociado con la RCC.

    Raises:
        ValueError: Si el género o el valor de RCC no son válidos.
    """

    # Validación de la RCC
    if not isinstance(rcc, (int, float)) or rcc <= 0:
        raise ValueError("El valor de RCC debe ser un número positivo.")

    # Validación del género
    if genero not in ['h', 'm']:
        raise ValueError("El género debe ser 'h' para hombre o 'm' para mujer.")

    # Interpretar RCC basado en el género
    if genero == 'h':
        if rcc > UMBRAL_RIESGO_ALTO_HOMBRE:
            return "Alto riesgo"
        elif UMBRAL_RIESGO_MODERADO_HOMBRE < rcc <= UMBRAL_RIESGO_ALTO_HOMBRE:
            return "Moderado riesgo"
        else:
            return "Bajo riesgo"
    else:
        if rcc > UMBRAL_RIESGO_ALTO_MUJER:
            return "Alto riesgo"
        elif UMBRAL_RIESGO_MODERADO_MUJER < rcc <= UMBRAL_RIESGO_ALTO_MUJER:
            return "Moderado riesgo"
        else:
            return "Bajo riesgo"

def calcular_relacion_cintura_cadera(cintura: Union[int, float], cadera: Union[int, float]) -> float:
    """
    Calcula la relación cintura-cadera (RCC), un indicador de la distribución de grasa corporal.

    Args:
        cintura (int | float): Medida de la cintura en centímetros.
        cadera (int | float): Medida de la cadera en centímetros.

    Returns:
        float: La relación cintura-cadera calculada.

    Raises:
        ValueError: Si la cintura o la cadera no son válidas.
    """

# validar la medida de la cintura
    if not isinstance(cintura, (int, float)) or cintura <= 0:
        raise ValueError("La cintura debe ser un número positivo.")

# validar la medida de la cadera
    if not isinstance(cadera, (int, float)) or cadera <= 0:
        raise ValueError("La cadera debe ser un número positivo y mayor que 0.")

# calcular la relación cintura-cadera
    return cintura / cadera


def calcular_ratio_cintura_altura(cintura: Union[int, float], altura: Union[int, float]) -> float:
    """
    Calcula el ratio cintura-altura, un indicador de riesgo de salud metabólica.

    Args:
        cintura (int | float): Medida de la cintura en centímetros.
        altura (int | float): Altura del usuario en centímetros.

    Returns:
        float: Ratio cintura-altura calculado.

    Raises:
        ValueError: Si la cintura o la altura no son válidas.
    """

    # Validar la medida de la cintura
    if not isinstance(cintura, (int, float)) or cintura <= 0:
        raise ValueError("La cintura debe ser un número positivo.")

    # Validar la medida de la altura
    if not isinstance(altura, (int, float)) or altura <= 0:
        raise ValueError("La altura debe ser un número positivo y mayor que 0.")

    # Calcular el ratio cintura-altura
    return cintura / altura


def interpretar_ratio_cintura_altura(ratio: Union[int, float]) -> str:
    """
    Interpreta el ratio cintura-altura para evaluar el riesgo metabólico y posibles riesgos cardiovasculares.

    Args:
        ratio (int | float): Ratio cintura-altura calculado.

    Returns:
        str: Interpretación del nivel de riesgo metabólico basado en el ratio.

    Raises:
        ValueError: Si el ratio no es válido.
    """

    # Validar que el ratio sea un número positivo
    if not isinstance(ratio, (int, float)) or ratio <= 0:
        raise ValueError("El ratio cintura-altura debe ser un número positivo.")

    # Interpretar el riesgo basado en el ratio
    if ratio >= 0.6:
        return "Alto riesgo"
    elif 0.5 <= ratio < 0.6:
        return "Moderado riesgo"
    else:
        return "Bajo riesgo"


def calcular_calorias_diarias(tmb: Union[int, float], objetivo: str) -> float:
    """
    Calcula las calorías diarias necesarias basadas en la TMB y el objetivo nutricional.

    Args:
        tmb (int | float): Tasa Metabólica Basal calculada.
        objetivo (str): Objetivo nutricional ('mantener', 'perder', 'ganar').

    Returns:
        float: Calorías diarias ajustadas según el objetivo.

    Raises:
        ValueError: Si la TMB no es válida o el objetivo no es reconocido.
    """

    # Validar que la TMB sea un número positivo
    if not isinstance(tmb, (int, float)) or tmb <= 0:
        raise ValueError("La TMB debe ser un número positivo.")

    # Validar el objetivo
    if objetivo not in ['mantener', 'perder', 'ganar']:
        raise ValueError("El objetivo debe ser 'mantener', 'perder' o 'ganar'.")

    # Calcular calorías según el objetivo
    if objetivo == 'mantener':
        return tmb * 1.2  # Factor de actividad moderado
    elif objetivo == 'perder':
        return tmb * 1.2 * 0.8  # 20% de reducción calórica
    elif objetivo == 'ganar':
        return tmb * 1.2 * 1.2  # 20% de aumento calórico


def calcular_macronutrientes(calorias: Union[int, float], objetivo: str) -> Tuple[float, float, float]:
    """
    Calcula la distribución de macronutrientes basada en las calorías diarias y el objetivo nutricional.

    Args:
        calorias (int | float): Calorías diarias recomendadas.
        objetivo (str): Objetivo nutricional ('mantener', 'perder', 'ganar').

    Returns:
        tuple: Gramos de proteínas, carbohidratos y grasas recomendados diariamente.

    Raises:
        ValueError: Si las calorías no son válidas o el objetivo no es reconocido.
    """

    # Validar que las calorías sean un número positivo
    if not isinstance(calorias, (int, float)) or calorias <= 0:
        raise ValueError("Las calorías deben ser un número positivo.")

    # Validar el objetivo
    if objetivo not in ['mantener', 'perder', 'ganar']:
        raise ValueError("El objetivo debe ser 'mantener', 'perder' o 'ganar'.")

    # Calcular la distribución de macronutrientes según el objetivo
    if objetivo == 'mantener':
        proteinas = (calorias * 0.30) / 4
        carbohidratos = (calorias * 0.40) / 4
        grasas = (calorias * 0.30) / 9
    elif objetivo == 'perder':
        proteinas = (calorias * 0.50) / 4
        carbohidratos = (calorias * 0.30) / 4
        grasas = (calorias * 0.20) / 9
    elif objetivo == 'ganar':
        proteinas = (calorias * 0.30) / 4
        carbohidratos = (calorias * 0.50) / 4
        grasas = (calorias * 0.20) / 9

    return float(proteinas), float(carbohidratos), float(grasas)


def guardar_datos(cliente_data: Dict[str, any]) -> bool:
    """
    Guarda los datos del cliente en la base de datos. Asegura que todos los campos necesarios estén presentes y sean válidos.

    Args:
        cliente_data (dict): Un diccionario con todos los datos del cliente, incluyendo nombre, medidas corporales, y resultados de cálculos.

    Returns:
        bool: True si los datos se guardaron correctamente, False si ocurrió un error.
    """

    try:
        # Validar que todos los campos requeridos estén presentes
        campos_requeridos = ['nombre', 'fecha', 'peso', 'altura', 'edad', 'genero', 'cintura', 'cadera',
                             'cuello', 'tmb', 'porcentaje_grasa', 'peso_grasa', 'masa_muscular', 'agua_total',
                             'ffmi', 'peso_min', 'peso_max', 'sobrepeso', 'rcc', 'ratio_cintura_altura',
                             'calorias_diarias', 'proteinas', 'carbohidratos', 'grasas']

        for campo in campos_requeridos:
            if campo not in cliente_data:
                raise ValueError(f"Falta el campo requerido: {campo}")

        # Validar que ciertos valores numéricos sean positivos
        valores_numericos = ['peso', 'altura', 'edad', 'cintura', 'cadera', 'cuello', 'tmb', 'porcentaje_grasa',
                             'peso_grasa', 'masa_muscular', 'agua_total', 'ffmi', 'peso_min', 'peso_max',
                             'sobrepeso', 'rcc', 'ratio_cintura_altura', 'calorias_diarias', 'proteinas',
                             'carbohidratos', 'grasas']

        for valor in valores_numericos:
            if not isinstance(cliente_data[valor], (int, float)) or cliente_data[valor] <= 0:
                raise ValueError(f"El valor de {valor} debe ser un número positivo.")

        # Crear el objeto cliente
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
            agua_total=cliente_data['agua_total'],
            ffmi=cliente_data['ffmi'],
            peso_min=cliente_data['peso_min'],
            peso_max=cliente_data['peso_max'],
            sobrepeso=cliente_data['sobrepeso'],
            rcc=cliente_data['rcc'],
            ratio_cintura_altura=cliente_data['ratio_cintura_altura'],
            calorias_diarias=cliente_data['calorias_diarias'],
            proteinas=cliente_data['proteinas'],
            carbohidratos=cliente_data['carbohidratos'],
            grasas=cliente_data['grasas']
        )

        # Guardar en la base de datos
        session.add(cliente)
        session.commit()
        print("Datos guardados exitosamente.")
        return True

    except ValueError as ve:
        print(f"Error de validación: {ve}")
        return False

    except Exception as e:
        session.rollback()
        print(f"Error al guardar datos: {e}")
        return False

# Configuración de logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def recuperar_historial() -> List[Cliente]:
    """
    Recupera el historial completo de clientes de la base de datos.

    Returns:
        list: Una lista de objetos Cliente, cada uno representando un registro histórico de un cliente.
    """
    try:
        historial = session.query(Cliente).all()
        return historial
    except Exception as e:
# Registrar el error en el log
        logging.error(f"Error al recuperar historial: {e}")
        return []
