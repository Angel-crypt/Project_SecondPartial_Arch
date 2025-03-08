from flask_bcrypt import Bcrypt
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import User
from controllers import Controller


bcrypt = Bcrypt()


class UserController(Controller):
    def __init__(self, supabase_client):
        super().__init__(supabase_client, "users")

    def register_user(self, name, password):
        existing_user = self.supabase.table(
            self.table).select("*").eq("name", name).execute()
        if existing_user.data:
            print("El usuario ya existe.")
            return False
        
        new_user = User(name, password)
        try:
            response = self.supabase.table(self.table).insert({
                "name": new_user.name,
                "password": new_user.password
            }).execute()
            print("Usuario registrado exitosamente.")
            return response.data is not None and len(response.data) > 0
        except Exception as e:
            print(f"Error al registrar el usuario: {e}")
            return False

    def login_user(self, name, password):
        # Buscar el usuario por nombre
        user_data = self.supabase.table(self.table).select(
            "*").eq("name", name).execute()
        if user_data.data:
            stored_password_hash = user_data.data[0]['password']

            if bcrypt.check_password_hash(stored_password_hash, password):
                print("Login exitoso.")
                return True
            else:
                print("Contraseña incorrecta.")
                return False
        else:
            print("Usuario no encontrado.")
            return False
