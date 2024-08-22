import tkinter as tk
from tkinter import messagebox
from models import Usuario
from calculadora import realizar_calculos


# Clase principal de la aplicación
class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis Composición Corporal")

        # Ventana de login
        self.login_frame = tk.Frame(root)
        self.login_frame.pack(pady=50)

        tk.Label(self.login_frame, text="Usuario:").grid(row=0, column=0)
        self.usuario_entry = tk.Entry(self.login_frame)
        self.usuario_entry.grid(row=0, column=1)

        tk.Label(self.login_frame, text="Contraseña:").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show='*')
        self.password_entry.grid(row=1, column=1)

        tk.Button(self.login_frame, text="Iniciar Sesión", command=self.iniciar_sesion).grid(row=2, column=0, columnspan=2)

        self.usuario_modelo = Usuario()

    def iniciar_sesion(self):
        usuario = self.usuario_entry.get()
        password = self.password_entry.get()

        if self.usuario_modelo.verificar_usuario(usuario, password):
            messagebox.showinfo("Login", "Inicio de sesión exitoso")
            self.mostrar_interfaz_principal()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def mostrar_interfaz_principal(self):
        # Ocultar la ventana de login
        self.login_frame.pack_forget()

        # Mostrar ventana principal (interfaz para los cálculos)
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=50)

        tk.Label(self.main_frame, text="Ingrese sus datos para el análisis:").grid(row=0, column=0, columnspan=2)
        # Aquí agregarás los campos de entrada y botones para calcular y mostrar los resultados

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()

