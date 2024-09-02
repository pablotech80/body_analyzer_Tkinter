from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import bcrypt

Base = declarative_base()

class Usuario(Base):

    """
        Representa un usuario en la base de datos, incluyendo administrador(admin no se ha configurado todavía)
        y usuarios normales.

        Atributos:
            id (Integer): Clave primaria, identificador único del usuario.
            username (String(50)): Nombre de usuario, debe ser único.
            password (String(255)): Contraseña del usuario, almacenada de manera segura.
            is_admin (Boolean): Indica si el usuario tiene privilegios de administrador.

        Métodos:
            set_password(self, password): Encripta y establece la contraseña del usuario.
            check_password(self, password): Verifica si una contraseña proporcionada coincide con la almacenada.
        """
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
    """
        Representa un cliente en la base de datos, almacenando información detallada
        sobre su composición corporal y métricas relacionadas.

        Atributos:
            id (Integer): Clave primaria, identificador único del cliente.
            nombre (String): Nombre del cliente.
            fecha (DateTime): Fecha del registro de datos.
            peso (Float): Peso del cliente en kilogramos.
            altura (Float): Altura del cliente en centímetros.
            edad (Integer): Edad del cliente.
            genero (String(1)): Género del cliente, 'h' para hombres, 'm' para mujeres.
            cintura (Float): Medida de la cintura del cliente.
            cadera (Float): Medida de la cadera del cliente.
            cuello (Float): Medida del cuello del cliente.
            tmb (Float): Tasa Metabólica Basal calculada.
            porcentaje_grasa (Float): Porcentaje de grasa corporal.
            peso_grasa (Float): Peso de grasa corporal en kilogramos.
            masa_muscular (Float): Masa muscular del cliente en kilogramos.
            agua_total (Float): Total de agua corporal en litros.
            ffmi (Float): Índice de Masa Libre de Grasa.
            peso_min (Float): Peso mínimo saludable calculado.
            peso_max (Float): Peso máximo saludable calculado.
            sobrepeso (Float): Sobrepeso calculado.
            rcc (Float): Relación cintura-cadera.
            ratio_cintura_altura (Float): Ratio cintura-altura.
            calorias_diarias (Float): Calorías diarias recomendadas.
            proteinas (Float): Gramos de proteínas recomendados diariamente.
            carbohidratos (Float): Gramos de carbohidratos recomendados diariamente.
            grasas (Float): Gramos de grasas recomendados diariamente.
        """
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
    ffmi = Column(Float)
    peso_min = Column(Float)
    peso_max = Column(Float)
    sobrepeso = Column(Float)
    rcc = Column(Float)
    ratio_cintura_altura = Column(Float)
    calorias_diarias = Column(Float)
    proteinas = Column(Float)
    carbohidratos = Column(Float)
    grasas = Column(Float)


'''Configuración de la base de datos'''

engine = create_engine('sqlite:///clientes.db')
Base.metadata.create_all(engine)

'''Creo una sesion en la base de datos'''

Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Base de datos creada.")