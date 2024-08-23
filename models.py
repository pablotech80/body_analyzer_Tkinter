from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración base de datos
Base = declarative_base()

# Definición del modelo Cliente
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

