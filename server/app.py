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
    ''' Registra un usuario en la base de datos '''
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
    ''' Inicia sesión de un usuario en la base de datos '''
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
    reemplazar por el caracter '%20'
    Ejemplo:
    "name": "Partido Revolucionario Independiente"
        Convertir a:
    "name": "Partido%20Revolucionario%20Independiente"
    
    Si el partido que se desea eliminar tiene representantes o afiliados,
    el servidor responderá con un mensaje de error y el código 400 (Bad Request), es necesario confirmar la eliminación
    enviando el parámetro 'confirm' con el valor 'true'
    Ejemplo:
    /parties/1?confirm=true
'''

#* Serializa un partido y convierlo en un objeto JSON
#? Serializar es convertir un objeto en un formato que se pueda transmitir o almacenar
def serialize_party(party):
    ''' Serializa un partido y lo convierte en un objeto JSON '''
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
    ''' Obtiene todos los partidos de la base de datos '''
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
    ''' Obtiene un partido por su ID '''
    # Obtener el partido por su ID
    party = party_controller.get_party_by_id(id)
    # Serializar el partido
    return serialize_party(party)

#* Obtener por nombre
@app.route('/parties/name/<string:name>', methods=['GET'])
def get_party_by_name(name):
    ''' Obtiene un partido por su nombre '''
    # Obtener el partido por su nombre
    party = party_controller.get_party_by_name(name)
    # Serializar el partido
    return serialize_party(party)

#* Obtener por siglas
@app.route('/parties/acronym/<string:acronym>', methods=['GET'])
def get_party_by_acronym(acronym):
    ''' Obtiene un partido por sus siglas '''
    # Obtener el partido por sus siglas
    party = party_controller.get_party_by_acronym(acronym)
    # Serializar el partido
    return serialize_party(party)

#* Crear un partido
@app.route('/parties', methods=['POST'])
def create_party():
    ''' Crea un partido en la base de datos '''
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
    response_data = result.to_dict()
    response_data["ID"] = result.id
    return jsonify(response_data), status_code

#* Actualizar un partido
@app.route('/parties/<int:id>', methods=['PUT'])
def update_party(id):
    ''' Actualiza un partido en la base de datos '''
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
    response_data = result.to_dict()
    response_data["ID"] = result.id
    return jsonify(response_data), status_code

#* Eliminar un partido
@app.route('/parties/<int:id>', methods=['DELETE'])
def delete_party(id):
    ''' Elimina un partido de la base de datos '''
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

''' Rutas para manejar Afiliados '''

'''
    Cuando se pide la data, se espera recibir un 
    JSON con los datos del afiliados
    Ejemplo:
    {
        "name": "Juan",
        "id_card": "123456",
        "birth_date": "2000-03-12",
        "enrollment_date": "2025-03-6",
        "id_party": 1
    }
    
    Si el nombre del afiliados tiene espacios, se debe
    reemplazar por el caracter '%20'
    Ejemplo:
    "name": "Juan Perez"
        Convertir a:
    "name": "Juan%20Perez"
    
    Para poder eliminar un afiliados, es necesario confirmar la eliminación
    enviando el parámetro 'confirm' con el valor 'true'
    Ejemplo:
    /representatives/1?confirm=true
'''

# * Serializa un afiliado y convierlo en un objeto JSON
def serialize_affiliate(affiliate):
    ''' Serializa un afiliado y lo convierte en un objeto JSON '''
    if not affiliate:
        return jsonify({'error': 'Afiliado no encontrado'}), 404
    return jsonify({
        "ID": affiliate.id,
        "Nombre": affiliate.name,
        "Numero de documento": affiliate.id_card,
        "Fecha de nacimiento": affiliate.birth_date,
        "Fecha de inscripcion": affiliate.enrollment_date,
        "ID Partido": affiliate.id_party,
        "Nombre Partido": affiliate_controller.get_name_party(affiliate.id_party)
    })

# * Obtener todos los afiliados
@app.route('/affiliates', methods=['GET'])
def get_all_affiliates():
    ''' Obtiene todos los afiliados de la base de datos '''
    affiliates = affiliate_controller.get_all_affiliates()
    if affiliates is None or not affiliates:
        return jsonify({"message": "No se encontraron afiliados."}), 404
    return jsonify([{
        "ID": affiliate.id,
        "Nombre": affiliate.name,
        "Numero de documento": affiliate.id_card,
        "Fecha de nacimiento": affiliate.birth_date,
        "Fecha de inscripcion": affiliate.enrollment_date,
        "ID Partido": affiliate.id_party,
        "Nombre Partido": affiliate_controller.get_name_party(affiliate.id_party)
    } for affiliate in affiliates])

# * Obtener un afiliado por su ID
@app.route('/affiliates/id/<int:id>', methods=['GET'])
def get_affiliate_by_id(id):
    ''' Obtiene un afiliado por su ID '''
    affiliate = affiliate_controller.get_affiliate_by_id(id)
    return serialize_affiliate(affiliate)

# * Obtener un afiliado por su nombre
@app.route('/affiliates/name/<string:name>', methods=['GET'])
def get_affiliate_by_name(name):
    ''' Obtiene un afiliado por su nombre '''
    affiliate = affiliate_controller.get_affiliate_by_name(name)
    return serialize_affiliate(affiliate)

# * Obtener afiliados por partido
@app.route('/affiliates/party/<int:id_party>', methods=['GET'])
def get_affiliate_by_party(id_party):
    ''' Obtiene los afiliados de un partido '''
    party = affiliate_controller.get_name_party(id_party)
    if party == "Partido no encontrado.":
        return jsonify({"message": "Partido no encontrado."}), 404
    affiliates = affiliate_controller.get_affiliate_by_party(id_party)
    return jsonify([{
        "ID": affiliate.id,
        "Nombre": affiliate.name,
        "Numero de documento": affiliate.id_card,
        "Fecha de nacimiento": affiliate.birth_date,
        "Fecha de inscripcion": affiliate.enrollment_date,
        "ID Partido": affiliate.id_party,
        "Nombre Partido": party
    } for affiliate in affiliates])

# * Crear un afiliado
@app.route('/affiliates', methods=['POST'])
def create_affiliate():
    ''' Crea un afiliado en la base de datos '''
    data = request.json
    new_affiliate = Affiliate(**data)
    result, status_code = affiliate_controller.create_affiliate(new_affiliate)
    if isinstance(result, dict) and 'error' in result:
        return jsonify(result), status_code
    # Aquí se modifica para incluir el ID en la respuesta
    response_data = result.to_dict()  # Convierte el afiliado a un diccionario
    response_data["ID"] = result.id  # Añade el ID al diccionario

    return jsonify(response_data), status_code

# * Actualizar un partido
@app.route('/affiliates/<int:id>', methods=['PUT'])
def update_affiliate(id):
    ''' Actualiza un afiliado en la base de datos '''
    # Obtener los datos JSON de la solicitud
    data = request.json

    # Buscar si el afiliado existe
    affiliate_to_update = affiliate_controller.get_affiliate_by_id(id)
    if not affiliate_to_update:
        return jsonify({'error': 'Afiliado no encontrado'}), 404
    
    # Actualizar los campos del afiliado
    data['id'] = id
    updated_affiliate = Affiliate(**data)
    
    # Intentar actualizar el afiliado
    result, status_code = affiliate_controller.update_affiliate(updated_affiliate)
    
    # Error
    if isinstance(result, dict) and 'error' in result:
        return jsonify(result), status_code
    
    response_data = result.to_dict()
    response_data["ID"] = result.id
    
    # Actualización exitosa
    return jsonify(response_data), status_code

# * Eliminar un afiliado
@app.route('/affiliates/<int:id>', methods=['DELETE'])
def delete_affiliate(id):
    ''' Elimina un afiliado de la base de datos '''
    # Verificar si se confirma la eliminación
    confirm_deletion = request.args.get('confirm', 'false').lower() == 'true'
    
    # Llamar al controlador para intentar eliminar el afiliado
    success, message = affiliate_controller.delete_affiliate(id, confirm_deletion)
    
    if success:
        # Si se eliminó correctamente, retornamos el código de éxito 204 (No Content)
        return jsonify({'success': message}), 200
    else:
        # Si no se pudo eliminar, retornamos el código 400 (Bad Request) o 404 (Not Found)
        return jsonify({'error': message}), 400 if "confirmación" in message else 404


''' Rutas para manejar representantes '''

'''
    Cuando se pide la data, se espera recibir un 
    JSON con los datos del representante
    Ejemplo:
    {
        "name": "Juan",
        "id_card": "123456",
        "birth_date": "2000-03-12",
        "enrollment_date": "2025-03-6",
        "id_party": 1,
        "party_position": "Presidente"
    }
    
    Si el nombre del representante tiene espacios, se debe
    reemplazar por el caracter '%20'
    Ejemplo:
    "name": "Juan Perez"
        Convertir a:
    "name": "Juan%20Perez"
    
    Para poder eliminar un representante, es necesario confirmar la eliminación
    enviando el parámetro 'confirm' con el valor 'true'
    Ejemplo:
    /representatives/1?confirm=true
'''

# * Serializa un representante y convierlo en un objeto JSON
def serialize_representative(representative):
    ''' Serializa un representante y lo convierte en un objeto JSON '''
    if not representative:
        return jsonify({'error': 'Representante no encontrado'}), 404
    return jsonify({
        "ID": representative.id,
        "Nombre": representative.name,
        "Numero de documento": representative.id_card,
        "Fecha de nacimiento": representative.birth_date,
        "Fecha de inscripcion": representative.enrollment_date,
        "ID Partido": representative.id_party,
        "Nombre Partido": representative_controller.get_name_party(representative.id_party),
        "Posicion Partido": representative.party_position
    })

# * Obtener todos los representantes
@app.route('/representatives', methods=['GET'])
def get_all_representatives():
    ''' Obtiene todos los representantes de la base de datos '''
    representatives = representative_controller.get_all_representatives()
    if representatives is None or not representatives:
        return jsonify({"message": "No se encontraron representantes."}), 404
    return jsonify([{
        "ID": representative.id,
        "Nombre": representative.name,
        "Numero de documento": representative.id_card,
        "Fecha de nacimiento": representative.birth_date,
        "Fecha de inscripcion": representative.enrollment_date,
        "ID Partido": representative.id_party,
        "Nombre Partido": representative_controller.get_name_party(representative.id_party),
        "Posicion Partido": representative.party_position
    } for representative in representatives])

# * Obtener un representante por su ID
@app.route('/representatives/id/<int:id>', methods=['GET'])
def get_representative_by_id(id):
    ''' Obtiene un representante por su ID '''
    representative = representative_controller.get_representative_by_id(id)
    return serialize_representative(representative)

# * Obtener un representante por su nombre
@app.route('/representatives/name/<string:name>', methods=['GET'])
def get_representative_by_name(name):
    ''' Obtiene un representante por su nombre '''
    representative = representative_controller.get_representative_by_name(name)
    return serialize_representative(representative)

# * Obtener representantes por partido
@app.route('/representatives/party/<int:id_party>', methods=['GET'])
def get_representative_by_party(id_party):
    ''' Obtiene los representantes de un partido '''
    party = representative_controller.get_name_party(id_party)
    if party == "Partido no encontrado.":
        return jsonify({"message": "Partido no encontrado."}), 404
    representatives = representative_controller.get_representative_by_party(id_party)
    return jsonify([{
        "ID": representative.id,
        "Nombre": representative.name,
        "Numero de documento": representative.id_card,
        "Fecha de nacimiento": representative.birth_date,
        "Fecha de inscripcion": representative.enrollment_date,
        "ID Partido": representative.id_party,
        "Nombre Partido": party,
        "Posicion Partido": representative.party_position
    } for representative in representatives])

# * Crear un representante
@app.route('/representatives', methods=['POST'])
def create_representative():
    ''' Crea un representante en la base de datos '''
    data = request.json
    new_representative = Representative(**data)
    result, status_code = representative_controller.create_representative(new_representative)
    if isinstance(result, dict) and 'error' in result:
        return jsonify(result), status_code
    response_data = result.to_dict()
    response_data["ID"] = result.id
    return jsonify(response_data), status_code

# * Actualizar un representante
@app.route('/representatives/<int:id>', methods=['PUT'])
def update_representative(id):
    ''' Actualiza un representante en la base de datos '''
    data = request.json
    representative_to_update = representative_controller.get_representative_by_id(id)
    if not representative_to_update:
        return jsonify({'error': 'Representante no encontrado'}), 404
    data['id'] = id
    updated_representative = Representative(**data)
    result, status_code = representative_controller.update_representative(updated_representative)
    if isinstance(result, dict) and 'error' in result:
        return jsonify(result), status_code
    response_data = result.to_dict()
    response_data["ID"] = result.id
    return jsonify(response_data), status_code

# * Eliminar un representante
@app.route('/representatives/<int:id>', methods=['DELETE'])
def delete_representative(id):
    ''' Elimina un representante de la base de datos '''
    confirm_deletion = request.args.get('confirm', 'false').lower() == 'true'
    success, message = representative_controller.delete_representative(id, confirm_deletion)
    if success:
        return jsonify({'success': message}), 200
    else:
        return jsonify({'error': message}), 400 if "confirmación" in message else 404

if __name__ == '__main__':
    app.run(debug=True)
