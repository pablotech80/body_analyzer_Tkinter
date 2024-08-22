import sqlite3

# Clase para manejar la base de datos de usuarios
class Usuario:
    def __init__(self):
        # Conexión a la base de datos SQLite
        self.conn = sqlite3.connect("usuarios.db")
        self.cursor = self.conn.cursor()
        # Crear tabla si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               nombre TEXT NOT NULL,
                               password TEXT NOT NULL,
                               historial TEXT)''')
        self.conn.commit()

    def registrar_usuario(self, nombre, password):
        # Insertar nuevo usuario
        try:
            self.cursor.execute("INSERT INTO usuarios (nombre, password) VALUES (?, ?)", (nombre, password))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error en la base de datos: {e}")

    def verificar_usuario(self, nombre, password):
        # Verificar si el usuario y la contraseña coinciden
        self.cursor.execute("SELECT * FROM usuarios WHERE nombre=? AND password=?", (nombre, password))
        return self.cursor.fetchone()

    def guardar_historial(self, nombre, historial):
        # Guardar el historial de un usuario
        try:
            self.cursor.execute("UPDATE usuarios SET historial=? WHERE nombre=?", (historial, nombre))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error guardando historial: {e}")

    def cerrar_conexion(self):
        self.conn.close()
