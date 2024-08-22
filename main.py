import tkinter as tk
from tkinter import messagebox
from models import Usuario
from calculadora import realizar_calculos


class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis Composición Corporal")
        self.root.geometry("400x600")
        self.root.configure(bg='#f0f0f0')

        self.login_frame = tk.Frame(root, bg='#f0f0f0')
        self.login_frame.pack(pady=50)

        tk.Label(self.login_frame, text="Usuario:", bg='#f0f0f0').grid(row=0, column=0, pady=5)
        self.usuario_entry = tk.Entry(self.login_frame)
        self.usuario_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.login_frame, text="Contraseña:", bg='#f0f0f0').grid(row=1, column=0, pady=5)
        self.password_entry = tk.Entry(self.login_frame, show='*')
        self.password_entry.grid(row=1, column=1, pady=5)

        tk.Button(self.login_frame, text="Iniciar Sesión", command=self.iniciar_sesion).grid(row=2, column=0,
                                                                                             columnspan=2, pady=10)

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
        self.login_frame.pack_forget()
        self.main_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.main_frame.pack(pady=20, padx=20, fill='both', expand=True)

        campos = [
            ("Nombre", "nombre"),
            ("Edad", "edad"),
            ("Género", "genero"),
            ("Altura (cm)", "altura"),
            ("Peso (kg)", "peso"),
            ("Cintura (cm)", "cintura"),
            ("Cadera (cm)", "cadera"),
            ("Cuello (cm)", "cuello")
        ]

        self.entradas = {}
        for i, (label, var_name) in enumerate(campos):
            tk.Label(self.main_frame, text=label, bg='#f0f0f0').grid(row=i, column=0, sticky='e', padx=5, pady=5)
            self.entradas[var_name] = tk.Entry(self.main_frame)
            self.entradas[var_name].grid(row=i, column=1, sticky='w', padx=5, pady=5)

        tk.Button(self.main_frame, text="Calcular", command=self.calcular).grid(row=len(campos), column=0, pady=10)
        tk.Button(self.main_frame, text="Limpiar", command=self.limpiar_campos).grid(row=len(campos), column=1, pady=10)

        self.resultado_text = tk.Text(self.main_frame, height=10, width=50)
        self.resultado_text.grid(row=len(campos) + 1, column=0, columnspan=2, pady=10)

    def calcular(self):
        try:
            datos = {key: float(entry.get()) if key not in ['nombre', 'genero'] else entry.get()
                     for key, entry in self.entradas.items()}

            resultados = realizar_calculos(datos)

            self.resultado_text.delete('1.0', tk.END)
            for key, value in resultados.items():
                self.resultado_text.insert(tk.END, f"{key}: {value}\n")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def limpiar_campos(self):
        for entry in self.entradas.values():
            entry.delete(0, tk.END)
        self.resultado_text.delete('1.0', tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()