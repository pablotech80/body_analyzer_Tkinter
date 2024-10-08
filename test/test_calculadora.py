import math
import pytest
from calculadora import (
    calcular_tmb, calcular_imc, calcular_porcentaje_grasa, interpretar_imc,
    calcular_peso_saludable, calcular_peso_min, calcular_peso_max, interpretar_porcentaje_generico,
    calcular_sobrepeso, calcular_rcc, calcular_masa_muscular, calcular_ffmi,
    interpretar_ffmi, calcular_relacion_cintura_cadera, interpretar_rcc,
    calcular_ratio_cintura_altura, interpretar_ratio_cintura_altura,
    calcular_calorias_diarias, calcular_macronutrientes, interpretar_porcentaje_grasa
)

def test_calcular_tmb_hombre():
    """Prueba la función calcular_tmb para un hombre."""
    peso = 70
    altura = 175
    edad = 30
    genero = 'h'
    resultado_esperado = 88.362 + (13.397 * peso) + (4.799 * altura) - (5.677 * edad)
    resultado_obtenido = calcular_tmb(peso, altura, edad, genero)
    assert resultado_obtenido == pytest.approx(resultado_esperado, 0.01)

def test_calcular_tmb_mujer():
    """Prueba la función calcular_tmb para una mujer."""
    peso = 60
    altura = 165
    edad = 25
    genero = 'm'
    resultado_esperado = 447.593 + (9.247 * peso) + (3.098 * altura) - (4.330 * edad)
    resultado_obtenido = calcular_tmb(peso, altura, edad, genero)
    assert resultado_obtenido == pytest.approx(resultado_esperado, 0.01)

def test_calcular_imc():
    """Prueba la función calcular_imc para determinar el Índice de Masa Corporal."""
    peso = 70
    altura = 175
    altura_m = altura / 100
    resultado_esperado = peso / (altura_m ** 2)
    resultado_obtenido = calcular_imc(peso, altura)
    assert resultado_obtenido == pytest.approx(resultado_esperado, 0.01)

def test_calcular_porcentaje_grasa_hombre():
    """Prueba la función calcular_porcentaje_grasa para un hombre utilizando la fórmula de la Marina Estadounidense."""
    altura = 175
    peso = 90
    cuello = 40
    cintura = 80
    resultado_esperado = 495 / (1.0324 - 0.19077 * math.log10(cintura - cuello) + 0.15456 * math.log10(altura)) - 450
    resultado_obtenido = calcular_porcentaje_grasa('h', peso, altura, cintura, cuello)
    assert resultado_obtenido == pytest.approx(resultado_esperado, 0.01)

def test_calcular_porcentaje_grasa_mujer():
    """Prueba la función calcular_porcentaje_grasa para una mujer."""
    altura = 165
    peso = 60
    cuello = 35
    cintura = 70
    cadera = 95

    resultado_esperado = 495 / (1.29579 - 0.35004 * math.log10(cintura + cadera - cuello) + 0.22100 * math.log10(altura)) - 450
    resultado_obtenido = calcular_porcentaje_grasa('m', peso=peso, altura=altura, cintura=cintura, cuello=cuello, cadera=cadera)
    assert resultado_obtenido == pytest.approx(resultado_esperado, 0.01)


def test_interpretar_imc():
    """Prueba si la interpretación del IMC está correcta."""
    imc = 26
    ffmi = 20
    genero = 'm'
    interpretacion = interpretar_imc(imc, ffmi, genero)
    assert interpretacion == "El IMC es alto, pero puede estar influenciado por una alta masa muscular."

def test_calcular_peso_saludable():
    """Prueba la función calcular_peso_saludable."""
    altura = 175
    altura_m = altura / 100
    peso_min_esperado = 18.5 * (altura_m ** 2)
    peso_max_esperado = 24.9 * (altura_m ** 2)
    peso_min_obtenido, peso_max_obtenido = calcular_peso_saludable(altura)
    assert peso_min_obtenido == pytest.approx(peso_min_esperado, 0.01)
    assert peso_max_obtenido == pytest.approx(peso_max_esperado, 0.01)

def test_calcular_peso_min():
    """Prueba si el cálculo de peso mín. es correcto."""
    altura = 175
    altura_m = altura / 100
    peso_min_esperado = 18.5 * (altura_m ** 2)
    peso_min_obtenido = calcular_peso_min(altura)
    assert peso_min_obtenido == pytest.approx(peso_min_esperado, 0.01)

def test_calcular_peso_max():
    """Prueba si el cálculo de peso máx. es correcto."""
    altura = 175
    altura_m = altura / 100
    peso_max_esperado = 24.9 * (altura_m ** 2)
    peso_max_obtenido = calcular_peso_max(altura)
    assert peso_max_obtenido == pytest.approx(peso_max_esperado, 0.01)

def test_calcular_sobrepeso():
    """Prueba si la función calcular_sobrepeso es correcta."""

    # caso normal
    peso = 80
    altura = 175
    peso_max = calcular_peso_max(altura)
    sobrepeso_esperado = max(0, peso - peso_max)
    sobrepeso_obtenido = calcular_sobrepeso(peso, altura)
    assert sobrepeso_obtenido == pytest.approx(sobrepeso_esperado, 0.01), \
        f"El sobrepeso obtenido ({sobrepeso_obtenido}) no es igual al esperado ({sobrepeso_esperado})"

    # caso sin sobrepeso (peso = al peso max.)
    peso = peso_max
    sobrepeso_esperado = 0
    sobrepeso_obtenido = calcular_sobrepeso(peso, altura)
    assert sobrepeso_obtenido == pytest.approx(sobrepeso_esperado, 0.01), \
        f"El sobrepeso debería ser 0 si el peso es igual al peso máximo."

    # Caso sin sobrepeso (peso menor al peso máximo)
    peso = peso_max - 10
    sobrepeso_esperado = 0
    sobrepeso_obtenido = calcular_sobrepeso(peso, altura)
    assert sobrepeso_obtenido == pytest.approx(sobrepeso_esperado, 0.01), \
        "El sobrepeso debería ser 0 si el peso es menor al peso máximo"

    # Caso con altura o peso negativo (esperando una excepción)
    with pytest.raises(ValueError):
        calcular_sobrepeso(-70, 175)
    with pytest.raises(ValueError):
        calcular_sobrepeso(70, -175)

def test_calcular_rcc():
    """Prueba si la función calcular_rcc es correcta."""
    cintura = 80
    cadera = 100
    rcc_esperado = cintura / cadera
    rcc_obtenido = calcular_rcc(cintura, cadera)
    assert rcc_obtenido == pytest.approx(rcc_esperado, 0.01)

def test_calcular_masa_muscular():
    """Prueba si la función calcular_masa_muscular es correcta."""
    peso = 70
    porcentaje_grasa = 20
    masa_muscular_esperada = peso * ((100 - porcentaje_grasa) / 100)
    masa_muscular_obtenida = calcular_masa_muscular(peso, porcentaje_grasa)
    assert masa_muscular_obtenida == pytest.approx(masa_muscular_esperada, 0.01)

def test_calcular_ffmi():
    """Prueba si la función calcular_ffmi es correcta."""
    masa_muscular = 50
    altura = 175
    altura_m = altura / 100
    ffmi_esperado = masa_muscular / (altura_m ** 2)
    ffmi_obtenido = calcular_ffmi(masa_muscular, altura)
    assert ffmi_obtenido == pytest.approx(ffmi_esperado, 0.01)

def test_interpretar_ffmi_hombre():
    """Prueba si la interpretación del FFMI para hombres es correcta."""
    ffmi = 21
    genero = 'h'
    interpretacion = interpretar_ffmi(ffmi, genero)
    assert interpretacion == "Fuerte (Muy buena forma física)"

def test_calcular_relacion_cintura_cadera():
    """Prueba si la función calcular_relacion_cintura_cadera es correcta."""
    cintura = 80
    cadera = 100
    ratio_esperado = cintura / cadera
    ratio_obtenido = calcular_relacion_cintura_cadera(cintura, cadera)
    assert ratio_obtenido == pytest.approx(ratio_esperado, 0.01)

def test_interpretar_rcc_hombre():
    """Prueba si la interpretación del RCC para hombres es correcta."""
    rcc = 0.96
    genero = 'h'
    interpretacion = interpretar_rcc(rcc, genero)
    assert interpretacion == "Alto riesgo"

def test_calcular_ratio_cintura_altura():
    """Prueba si la función calcular_ratio_cintura_altura es correcta."""
    cintura = 80
    altura = 175
    ratio_esperado = cintura / altura
    ratio_obtenido = calcular_ratio_cintura_altura(cintura, altura)
    assert ratio_obtenido == pytest.approx(ratio_esperado, 0.01)

def test_interpretar_ratio_cintura_altura():
    """Prueba si la interpretación del ratio cintura-altura es correcta."""
    ratio = 0.55
    interpretacion = interpretar_ratio_cintura_altura(ratio)
    assert interpretacion == "Moderado riesgo"

def test_calcular_calorias_diarias():
    """Prueba si la función calcular_calorias_diarias es correcta."""
    tmb = 2000
    objetivo = 'mantener'
    calorias_esperadas = tmb * 1.2
    calorias_obtenidas = calcular_calorias_diarias(tmb, objetivo)
    assert calorias_obtenidas == pytest.approx(calorias_esperadas, 0.01)

def test_calcular_macronutrientes_mantener():
    """Prueba si la función calcular_macronutrientes devuelve el resultado según objetivo."""
    calorias = 2000
    objetivo = 'mantener'
    proteinas, carbohidratos, grasas = calcular_macronutrientes(calorias, objetivo)
    assert proteinas == pytest.approx((calorias * 0.30) / 4, 0.01)
    assert carbohidratos == pytest.approx((calorias * 0.40) / 4, 0.01)
    assert grasas == pytest.approx((calorias * 0.30) / 9, 0.01)

def test_interpretar_porcentaje_grasa_hombre():
    """Prueba si la función interpretar_porcentaje_grasa para hombres es correcta."""
    porcentaje_grasa = 30
    genero = 'h'
    interpretacion = interpretar_porcentaje_grasa(porcentaje_grasa, genero)
    assert interpretacion == "Alto"

def test_interpretar_porcentaje_generico():
    assert interpretar_porcentaje_generico(30, genero_val='h') == "Alto"
    assert interpretar_porcentaje_generico(8, genero_val='h') == "Bajo"
    assert interpretar_porcentaje_generico(15, genero_val='h') == "Normal"
    assert interpretar_porcentaje_generico(20, genero_val='m') == "Normal"
    assert interpretar_porcentaje_generico(35, genero_val='m') == "Alto"
    assert interpretar_porcentaje_generico(16, genero_val='m') == "Bajo"
