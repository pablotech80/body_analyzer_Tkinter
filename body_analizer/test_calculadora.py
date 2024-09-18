import unittest
import math
from calculadora import (
    calcular_tmb, calcular_imc, calcular_porcentaje_grasa,interpretar_imc,
    calcular_peso_saludable, calcular_peso_min, calcular_peso_max,
    calcular_sobrepeso, calcular_rcc, calcular_masa_muscular, calcular_ffmi,
    interpretar_ffmi, calcular_relacion_cintura_cadera, interpretar_rcc,
    calcular_ratio_cintura_altura, interpretar_ratio_cintura_altura,
    calcular_calorias_diarias, calcular_macronutrientes, interpretar_porcentaje_grasa
)

class TestCalculadora(unittest.TestCase):

    """Conjunto de pruebas para verificar la exactitud de las funciones
        matemáticas en el módulo calculadora."""
    def test_calcular_tmb_hombre(self):

        """Prueba la funcón calcular_tmb para un hombre."""
        peso = 70
        altura = 175
        edad = 30
        genero = 'h'
        resultado_esperado = 88.362 + (13.397 * peso) + (4.799 * altura) - (5.677 * edad)
        self.assertAlmostEqual(calcular_tmb(peso, altura, edad, genero), resultado_esperado, places=2)

    def test_calcular_tmb_mujer(self):

        """Prueba la funcón calcular_tmb para una mujer."""
        peso = 60
        altura = 165
        edad = 25
        genero = 'm'
        resultado_esperado = 447.593 + (9.247 * peso) + (3.098 * altura) - (4.330 * edad)
        self.assertAlmostEqual(calcular_tmb(peso, altura, edad, genero), resultado_esperado, places=2)

    def test_calcular_imc(self):

        """Prueba la función calcular_imc para determinar el Índice de Masa Corporal."""
        peso = 70
        altura = 175
        altura_m = altura / 100
        resultado_esperado = peso / (altura_m ** 2)
        self.assertAlmostEqual(calcular_imc(peso, altura), resultado_esperado, places=2)

    def test_calcular_porcentaje_grasa_hombre(self):

        """Prueba la función calcular_porcentaje_grasa para un hombre
        utilizando la fórmula de la Marina Estadounidense."""


        cintura = 80
        cadera = 90
        cuello = 40
        altura = 175
        genero = 'h'
        resultado_esperado = 495 / (1.0324 - 0.19077 * math.log10(cintura - cuello) + 0.15456 * math.log10(altura)) - 450
        self.assertAlmostEqual(calcular_porcentaje_grasa(cintura, cadera, cuello, altura, genero), resultado_esperado, places=2)


    def test_interpretar_imc(self):

        """Prueba si la interpretación del IMC está correcto"""
        imc = 26
        ffmi = 20
        genero = 'm'
        self.assertEqual(interpretar_imc(imc, ffmi, genero),
                         "El IMC es alto, pero puede estar influenciado "
                         "por una alta masa muscular.")

    def test_calcular_peso_saludable(self):

        """Prueba la función calcular_peso_saludable"""
        altura = 175
        altura_m = altura / 100
        peso_min_esperado = 18.5 * (altura_m ** 2)
        peso_max_esperado = 24.9 * (altura_m ** 2)
        self.assertAlmostEqual(calcular_peso_saludable(altura),
                               (peso_min_esperado, peso_max_esperado), places=2)

    def test_calcular_peso_min(self):

        """Prueba si el cálculo de peso mín es correcto"""
        altura = 175
        altura_m = altura / 100
        peso_min_esperado = 18.5 * (altura_m ** 2)
        self.assertAlmostEqual(calcular_peso_min(altura), peso_min_esperado, places=2)

    def test_calcular_peso_max(self):

        """Prueba si el cálculo de peso máx es correcto"""
        altura = 175
        altura_m = altura / 100
        peso_max_esperado = 24.9 * (altura_m ** 2)
        self.assertAlmostEqual(calcular_peso_max(altura), peso_max_esperado, places=2)

    def test_calcular_sobrepeso(self):

        """Prueba si la función calcular_sobrepeso es correcta."""
        peso = 80
        altura = 175
        peso_max = calcular_peso_max(altura)
        sobrepeso_esperado = max(0, peso - peso_max)
        self.assertAlmostEqual(calcular_sobrepeso(peso, altura), sobrepeso_esperado, places=2)

    def test_calcular_rcc(self):

        """prueba si la función calcular_rcc es correcta"""
        cintura = 80
        cadera = 100
        rcc_esperado = cintura / cadera
        self.assertAlmostEqual(calcular_rcc(cintura, cadera), rcc_esperado, places=2)

    def test_calcular_masa_muscular(self):

        """Prueba si la función calcular_masa_muscular es correcta"""
        peso = 70
        porcentaje_grasa = 20
        masa_muscular_esperada = peso * ((100 - porcentaje_grasa) / 100)
        self.assertAlmostEqual(calcular_masa_muscular(peso, porcentaje_grasa),
                               masa_muscular_esperada, places=2)

    def test_calcular_ffmi(self):

        """Prueba si la función calcular_ffmi es correcta"""
        masa_muscular = 50
        altura = 175
        altura_m = altura / 100
        ffmi_esperado = masa_muscular / (altura_m ** 2)
        self.assertAlmostEqual(calcular_ffmi(masa_muscular, altura), ffmi_esperado, places=2)

    def test_interpretar_ffmi_hombre(self):

        """Prueba si la función interpretar el ffmi es correcto"""
        ffmi = 21
        genero = 'h'
        self.assertEqual(interpretar_ffmi(ffmi, genero), "Fuerte (Muy buena forma física)")

    def test_calcular_relacion_cintura_cadera(self):

        """Prueba si la funcion rcc esta correcta"""
        cintura = 80
        cadera = 100
        ratio_esperado = cintura / cadera
        self.assertAlmostEqual(calcular_relacion_cintura_cadera(cintura, cadera),
                               ratio_esperado, places=2)

    def test_interpretar_rcc_hombre(self):

        """Prueba si la función que interpreta el rcc (hombre( es correcto"""
        rcc = 0.96
        genero = 'h'
        self.assertEqual(interpretar_rcc(rcc, genero), "Alto riesgo")

    def test_calcular_ratio_cintura_altura(self):

        """Prueba si la función ratio_cintura_cadera es correcto"""
        cintura = 80
        altura = 175
        ratio_esperado = cintura / altura
        self.assertAlmostEqual(calcular_ratio_cintura_altura(cintura, altura), ratio_esperado, places=2)

    def test_interpretar_ratio_cintura_altura(self):

        """Prueba si la interpretación de rca es correcto"""
        ratio = 0.55
        self.assertEqual(interpretar_ratio_cintura_altura(ratio), "Moderado riesgo")

    def test_calcular_calorias_diarias(self):

        """prueba si la función calcular_calorias_diarias es correcto"""
        tmb = 2000
        objetivo = 'mantener'
        calorias_esperadas = tmb * 1.2
        self.assertAlmostEqual(calcular_calorias_diarias(tmb, objetivo), calorias_esperadas, places=2)

    def test_calcular_macronutrientes_mantener(self):

        """Prueba si la función calcular_macronutrientes_mantener devuelve el resultado según objetivo"""
        calorias = 2000
        objetivo = 'mantener'
        proteinas, carbohidratos, grasas = calcular_macronutrientes(calorias, objetivo)
        self.assertAlmostEqual(proteinas, (calorias * 0.30) / 4, places=2)
        self.assertAlmostEqual(carbohidratos, (calorias * 0.40) / 4, places=2)
        self.assertAlmostEqual(grasas, (calorias * 0.30) / 9, places=2)

    def test_interpretar_porcentaje_grasa_hombre(self):

        """Prueba si la función interpreta de manera correcta el resultado del porcentaje_grasa"""
        porcentaje_grasa = 30
        genero = 'h'
        self.assertEqual(interpretar_porcentaje_grasa(porcentaje_grasa, genero), "Alto")

if __name__ == '__main__':
    unittest.main()

