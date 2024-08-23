import unittest
from unittest.mock import patch
import tkinter as tk
from main import calcular, validar_entradas, limpiar_campos

class TestMainFunctions(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        # Aquí deberías inicializar todas las variables globales que se usan en main.py
        global nombre, peso, altura, edad, genero, objetivo, proteina, carbohidrato, grasa, cadera, cintura, cuello
        nombre = tk.StringVar()
        peso = tk.StringVar()
        altura = tk.StringVar()
        edad = tk.StringVar()
        genero = tk.StringVar()
        objetivo = tk.StringVar()
        proteina = tk.StringVar()
        carbohidrato = tk.StringVar()
        grasa = tk.StringVar()
        cadera = tk.StringVar()
        cintura = tk.StringVar()
        cuello = tk.StringVar()

        # Inicializar variables de resultado
        global resultado_tmb, resultado_imc, resultado_porcentaje_grasa
        resultado_tmb = tk.StringVar()
        resultado_imc = tk.StringVar()
        resultado_porcentaje_grasa = tk.StringVar()
        # ... inicializar el resto de variables de resultado ...

    def tearDown(self):
        self.root.destroy()

    def test_validar_entradas(self):
        peso.set("70")
        altura.set("170")
        edad.set("30")
        genero.set("h")
        cintura.set("80")
        cuello.set("35")
        self.assertTrue(validar_entradas())

        peso.set("abc")  # Valor inválido
        self.assertFalse(validar_entradas())

    @patch('main.messagebox.showerror')
    def test_calcular(self, mock_showerror):
        # Configurar valores válidos
        peso.set("70")
        altura.set("170")
        edad.set("30")
        genero.set("h")
        cintura.set("80")
        cuello.set("35")
        objetivo.set("mantener")

        calcular()

        # Verificar que se hayan calculado algunos resultados
        self.assertNotEqual(resultado_tmb.get(), "")
        self.assertNotEqual(resultado_imc.get(), "")
        self.assertNotEqual(resultado_porcentaje_grasa.get(), "")

    def test_limpiar_campos(self):
        # Establecer algunos valores
        nombre.set("Test")
        peso.set("70")
        altura.set("170")

        limpiar_campos()

        # Verificar que los campos se hayan limpiado
        self.assertEqual(nombre.get(), "")
        self.assertEqual(peso.get(), "")
        self.assertEqual(altura.get(), "")

if __name__ == '__main__':
    unittest.main()