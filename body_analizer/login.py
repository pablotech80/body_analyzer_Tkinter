import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.orm import sessionmaker

from main import MainApplication
from models import Usuario, engine

Session = sessionmaker(bind=engine)

class LoginWindow:

    """Gestiona la interfaz de usuario para el proceso de inicio de sesión y registro.

    Permite a los usuarios ingresar o registrar credenciales para acceder a la aplicación.
    Inicializa con la ventana raíz y la función de aplicación principal para manejar el inicio de sesión exitoso.

    Atributos:
        root (tk.Tk): Ventana raíz de la aplicación.
        main_app (function): Función que se llama para iniciar la aplicación principal tras un inicio de sesión exitoso.
        frame (ttk.Frame): Marco que contiene los widgets de la interfaz de usuario.
        username (tk.StringVar): Variable de control para el nombre de usuario.
        password (tk.StringVar): Variable de control para la contraseña.
    """

    def __init__(self, root, main_app):

        """Inicializa la ventana de inicio de sesión con configuración básica y elementos de UI.

        Args:
            root (tk.Tk): La ventana raíz de la aplicación.
            main_app (function): Función para iniciar la aplicación principal.
        """
        self.root = root
        self.main_app = main_app
        self.root.title("Login - Análisis de Composición Corporal")

        self.frame = ttk.Frame(root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(self.frame, text="Usuario:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username = tk.StringVar()
        ttk.Entry(self.frame, textvariable=self.username).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(self.frame, text="Contraseña:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.password = tk.StringVar()
        ttk.Entry(self.frame, textvariable=self.password, show='*').grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

        ttk.Button(self.frame, text="Iniciar Sesión", command=self.login).grid(row=2, column=0, pady=10)
        ttk.Button(self.frame, text="Registrarse", command=self.register).grid(row=2, column=1, pady=10)

    def login(self):

        """Inicia sesión del usuario verificando las credenciales contra la base de datos."""
        username = self.username.get()
        password = self.password.get()

        session = Session()
        user = session.query(Usuario).filter_by(username=username).first()
        if user and user.check_password(password):
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
            self.root.destroy()  # Cierra la ventana de inicio de sesión
            self.main_app()  # Inicia la aplicación principal
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        session.close()

    def register(self):

        """Registra un nuevo usuario en la base de datos."""
        username = self.username.get()
        password = self.password.get()

        session = Session()
        existing_user = session.query(Usuario).filter_by(username=username).first()
        if existing_user:
            messagebox.showerror("Error", "El nombre de usuario ya existe")
        else:
            new_user = Usuario(username=username)
            new_user.set_password(password)
            session.add(new_user)
            session.commit()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente")
        session.close()
