'''
Este archivo contiene la configuración de la aplicación de Flask y la inicialización de los controladores de la aplicación.'''

# Importar las librerías necesarias
from flask import Flask, jsonify, request
from supabase import create_client
from dotenv import load_dotenv
import os
import sys

# Añadir el directorio padre al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Importar controladores y modelos
from controllers import PartyController, RepresentativeController, AffiliateController, UserController
from models import Party, Representative, Affiliate, User

# Cargar variables de entorno
load_dotenv()

# Inicializar la aplicación de Flask
app = Flask(__name__)

# Crear un cliente de Supabase
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
supabase = create_client(url, key)

# Inicialización de controladores
party_controller = PartyController(supabase)
representative_controller = RepresentativeController(supabase)
affiliate_controller = AffiliateController(supabase)
user_controller = UserController(supabase)

''' Rutas para manejar usuarios '''
'''
    Cuando se pide la data, se espera recibir un
    JSON con los datos del usuario
    Ejemplo:
    {
        "name": "Juan",
        "password": "123456"
    }
'''

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    password = data.get('password')
    success = user_controller.register_user(name, password)
    if success:
        return jsonify({'message': 'Usuario registrado exitosamente.'}), 201
    else:
        return jsonify({'message': 'Error al registrar el usuario.'}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    name = data.get('name')
    password = data.get('password')
    success = user_controller.login_user(name, password)
    if success:
        return jsonify({'message': 'Login exitoso.'}), 200
    else:
        return jsonify({'message': 'Error en el login.'}), 401


''' Rutas para manejar partidos '''

'''
    Cuando se pide la data, se espera recibir un 
    JSON con los datos del partido
    Ejemplo:
    {
        "name": "Partido Revolucionario Independiente",
        "acronym": "PRI",
        "fundation_date": "2000-03-12",
        "ideology": "Derecha"
    }
    
    Si el nombre del partido tiene espacios, se debe
    reemplazar por el caracter '%20' o '+'
    Ejemplo:
    "name": "Partido Revolucionario Independiente"
        Convertir a:
    "name": "Partido%20Revolucionario%20Independiente"
    "name": "Partido+Revolucionario+Independiente"
    
    Si el partido que se desea eliminar tiene representantes o afiliados,
    el servidor responderá con un mensaje de error y el código 400 (Bad Request), es necesario confirmar la eliminación
    enviando el parámetro 'confirm' con el valor 'true'
    Ejemplo:
    /parties/1?confirm=true
'''

#* Serializa un partido y convierlo en un objeto JSON
#? Serializar es convertir un objeto en un formato que se pueda transmitir o almacenar
def serialize_party(party):
    if not party:
        return jsonify({'error': 'Partido no encontrado'}), 404
    return jsonify({
        "ID": party.id,
        "Nombre": party.name,
        "Siglas": party.acronym,
        "Fundacion": party.fundation_date,
        "Ideologia": party.ideology
    })

#* Obtener todos los partidos
@app.route('/parties', methods=['GET'])
def get_all_parties():
    # Obtener todos los partidos
    parties = party_controller.get_all_parties()
    # Serializar los partidos
    return jsonify([{
        "ID": party.id,
        "Nombre": party.name,
        "Siglas": party.acronym,
        "Fundacion": party.fundation_date
    } for party in parties])

#* Obtener un partido por su ID
@app.route('/parties/id/<int:id>', methods=['GET'])
def get_party_by_id(id):
    # Obtener el partido por su ID
    party = party_controller.get_party_by_id(id)
    # Serializar el partido
    return serialize_party(party)

#* Obtener por nombre
@app.route('/parties/name/<string:name>', methods=['GET'])
def get_party_by_name(name):
    # Obtener el partido por su nombre
    party = party_controller.get_party_by_name(name)
    # Serializar el partido
    return serialize_party(party)

#* Obtener por siglas
@app.route('/parties/acronym/<string:acronym>', methods=['GET'])
def get_party_by_acronym(acronym):
    # Obtener el partido por sus siglas
    party = party_controller.get_party_by_acronym(acronym)
    # Serializar el partido
    return serialize_party(party)

#* Crear un partido
@app.route('/parties', methods=['POST'])
def create_party():
    # Recibir los datos del partido
    data = request.json
    # Crear un objeto de tipo Party
    new_party = Party(**data)

    # Crear el partido
    result, status_code = party_controller.create_party(new_party)
    # El resultado es un diccionario de error
    if isinstance(result, dict) and 'error' in result:
        return jsonify(result), status_code

    # Verificar si result es un diccionario (error)
    if isinstance(result, dict) and 'error' in result:
        return jsonify(result), status_code

    # Si el partido se creó correctamente, retornamos los datos del partido con código 201
    return jsonify(result.to_dict()), status_code

#* Actualizar un partido
@app.route('/parties/<int:id>', methods=['PUT'])
def update_party(id):
    # Obtener los datos JSON de la solicitud
    data = request.json

    # Buscar si el partido existe
    party_to_update = party_controller.get_party_by_id(id)
    if not party_to_update:
        return jsonify({'error': 'Partido no encontrado'}), 404

    # Actualizar los campos del partido
    data['id'] = id
    updated_party = Party(**data)

    # Intentar actualizar el partido
    result, status_code = party_controller.update_party(updated_party)

    # Si el resultado es un diccionario de error, devuelve el error con el código adecuado
    if isinstance(result, dict) and 'error' in result:
        return jsonify(result), status_code

    # Si la actualización fue exitosa, devuelve el partido actualizado con el código 200
    return jsonify(result.to_dict()), status_code

#* Eliminar un partido
@app.route('/parties/<int:id>', methods=['DELETE'])
def delete_party(id):
    # Verificar si se confirma la eliminación
    confirm_deletion = request.args.get('confirm', 'false').lower() == 'true'

    # Llamar al controlador para intentar eliminar el partido
    success, message = party_controller.delete_party(id, confirm_deletion)
    print(success, message)

    if success:
        # Si se eliminó correctamente, retornamos el código de éxito 204 (No Content)
        return jsonify({'success': message}), 200
    else:
        # Si no se pudo eliminar, retornamos el código 400 (Bad Request) o 404 (Not Found)
        return jsonify({'error': message}), 400 if "confirmación" in message else 404

if __name__ == '__main__':
    app.run(debug=True)
