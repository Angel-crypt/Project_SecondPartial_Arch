import os
import sys

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from supabase import create_client
from controllers import UserController

# Configuración de Supabase
url = 'https://tpgbsatkplqmdglpiuyz.supabase.co/'
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwZ2JzYXRrcGxxbWRnbHBpdXl6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDEyODU1NzAsImV4cCI6MjA1Njg2MTU3MH0.EvTW2Ktpqtl3FANUTT7Q3z_v-oYQN1kU-83PnF0AvPo'
supabase = create_client(url, key)

# Inicialización del controlador de usuarios
user_controller = UserController(supabase)


def register_user(name, password):
    user_controller.register_user(name, password)


def login_user(name, password):
    user_controller.login_user(name, password)


if __name__ == "__main__":
    # Prueba de registro
    '''print("Prueba de registro:")
    register_user("test_user", "test_password")
    register_user("Admin", "admin_pass")
    input()'''

    # Prueba de inicio de sesión
    print("\nPrueba de inicio de sesión:")
    login_user("Admin", "admin_pass")
    login_user("test_user", "test_password")
    input()

    '''# Prueba de inicio de sesión con contraseña incorrecta
    print("\nPrueba de inicio de sesión con contraseña incorrecta:")
    login_user("test_user", "wrong_password")
    input()

    # Prueba de registro de un usuario existente
    print("\nPrueba de registro de un usuario existente:")
    register_user("test_user", "test_password")
    input()'''
