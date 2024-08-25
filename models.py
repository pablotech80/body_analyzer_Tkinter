from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import bcrypt

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    fecha = Column(DateTime, nullable=False)
    peso = Column(Float, nullable=False)
    altura = Column(Float, nullable=False)
    edad = Column(Integer, nullable=False)
    genero = Column(String(1), nullable=False)
    cintura = Column(Float, nullable=False)
    cadera = Column(Float, nullable=False)
    cuello = Column(Float, nullable=False)
    tmb = Column(Float)
    porcentaje_grasa = Column(Float)
    peso_grasa = Column(Float)
    masa_muscular = Column(Float)
    agua_total = Column(Float)

# Configuración de la base de datos
engine = create_engine('sqlite:///clientes.db')
Base.metadata.create_all(engine)

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Base de datos creada.")