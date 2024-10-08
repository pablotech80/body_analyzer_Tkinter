

"""En este fichero guardaré todas las constantes
para las formulas matemáticas que no se deben modificar"""


# Constantes para el cálculo de TMB para hombres
VALOR_TMB_HOMBRE = 88.362
FACTOR_PESO_HOMBRE = 13.397
FACTOR_ALTURA_HOMBRE = 4.799
FACTOR_EDAD_HOMBRE = 5.677

# Constantes para el cálculo de TMB para mujeres
VALOR_TMB_MUJER = 447.593
FACTOR_PESO_MUJER = 9.247
FACTOR_ALTURA_MUJER = 3.098
FACTOR_EDAD_MUJER = 4.330

# Umbrales para hombres
HOMBRE_ALTO_THRESHOLD = 25
HOMBRE_BAJO_THRESHOLD = 6
alto_threshold = 25
bajo_threshold = 6
# Umbrales para mujeres
MUJER_ALTO_THRESHOLD = 32
MUJER_BAJO_THRESHOLD = 16
alto_threshold = 32
bajo_threshold = 16

# Constantes para calcular el agua total en hombres
AGUA_TOTAL_HOMBRE_BASE = 2.447
AGUA_TOTAL_HOMBRE_EDAD = 0.09156
AGUA_TOTAL_HOMBRE_ALTURA = 0.1074
AGUA_TOTAL_HOMBRE_PESO = 0.3362

# Constantes para calcular el agua total en mujeres
AGUA_TOTAL_MUJER_BASE = -2.097
AGUA_TOTAL_MUJER_ALTURA = 0.1069
AGUA_TOTAL_MUJER_PESO = 0.2466

# Rangos de IMC
IMC_MIN_SALUDABLE = 18.5
IMC_MAX_SALUDABLE = 24.9
IMC_SOBREPESO = 31.9
IMC_OBESIDAD_1 = 34.9
IMC_OBESIDAD_2 = 39.9
IMC_OB_MORBIDA = 44.9


# Umbrales de FFMI para hombres
FFMI_THRESHOLDS_HOMBRES = [
    (18, "Lejos del máximo potencial (pobre forma física)"),
    (19, "Cercano a la normalidad"),
    (20, "Normal"),
    (21, "Superior a la normalidad (buena forma física)"),
    (22.5, "Fuerte (Muy buena forma física)"),
    (24, "Muy fuerte (Excelente forma física). Cerca del máximo potencial."),
    (25.5, "Muy cerca del máximo potencial."),
    (27, "Potencial máximo natural alcanzado. Muy muy pocos llegan naturales"),
    (29, "Prácticamente imposible sin fármacos")
]

# Umbrales de FFMI para mujeres
FFMI_THRESHOLDS_MUJERES = [
    (13.5, "Lejos del máximo potencial (pobre forma física)"),
    (14.5, "Cercano a la normalidad"),
    (16, "Normal"),
    (17, "Superior a la normalidad (buena forma física)"),
    (18.5, "Fuerte (Muy buena forma física)"),
    (20, "Muy fuerte (Excelente forma física). Cerca del máximo potencial."),
    (21, "Muy cerca del máximo potencial."),
    (22, "Potencial máximo natural alcanzado. Muy muy pocos llegan naturales"),
    (23, "Prácticamente imposible sin fármacos")
]

# Umbrales de riesgo para hombres en relación cintura-cadera (RCC)
UMBRAL_RIESGO_ALTO_HOMBRE = 0.95
UMBRAL_RIESGO_MODERADO_HOMBRE = 0.90

# Umbrales de riesgo para mujeres en relación cintura-cadera (RCC)
UMBRAL_RIESGO_ALTO_MUJER = 0.85
UMBRAL_RIESGO_MODERADO_MUJER = 0.80


