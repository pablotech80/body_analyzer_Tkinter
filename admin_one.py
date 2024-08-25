from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Usuario
import getpass

engine = create_engine('sqlite:///clientes.db')
Session = sessionmaker(bind=engine)


def crear_admin():
    session = Session()

    username = input("Ingrese el nombre de usuario del administrador: ")
    password = getpass.getpass("Ingrese la contraseña del administrador: ")

    existing_user = session.query(Usuario).filter_by(username=username).first()
    if existing_user:
        print("Error: El nombre de usuario ya existe.")
        return

    new_admin = Usuario(username=username, is_admin=True)
    new_admin.set_password(password)
    session.add(new_admin)
    session.commit()
    print(f"Administrador '{username}' creado exitosamente.")
    session.close()


if __name__ == "__main__":
    crear_admin()