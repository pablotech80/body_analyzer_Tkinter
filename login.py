import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.orm import sessionmaker
from models import Usuario, engine

Session = sessionmaker(bind=engine)


class LoginWindow:
    def __init__(self, root, main_app):
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
        username = self.username.get()
        password = self.password.get()

        session = Session()
        user = session.query(Usuario).filter_by(username=username).first()
        if user and user.check_password(password):
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
            self.root.destroy()
            self.main_app()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        session.close()

    def register(self):
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