from flask import Flask, jsonify, request
from controllers.party_controller import PartyController
from controllers.representative_controller import RepresentativeController
from controllers.affiliate_controller import AffiliateController
from supabase import create_client

app = Flask(__name__)

# Configuración de Supabase
url = 'https://tpgbsatkplqmdglpiuyz.supabase.co/'
key = 'tu_clave_de_supabase'
supabase = create_client(url, key)

# Inicialización de controladores
party_controller = PartyController(supabase)
representative_controller = RepresentativeController(supabase)
affiliate_controller = AffiliateController(supabase)

# Rutas para manejar partidos



@app.route('/parties/<int:id>', methods=['DELETE'])
def delete_party(id):
    success = party_controller.delete_party(id)
    return jsonify({'success': success}), 204 if success else 404

# Rutas para manejar representantes


@app.route('/representatives', methods=['GET'])
def get_all_representatives():
    representatives = representative_controller.get_all_representatives()
    return jsonify([rep.to_dict() for rep in representatives])

# Rutas para manejar afiliados


@app.route('/affiliates', methods=['GET'])
def get_all_affiliates():
    affiliates = affiliate_controller.get_all_affiliates()
    return jsonify([aff.to_dict() for aff in affiliates])


# Iniciar el servidor
if __name__ == '__main__':
    app.run(debug=True)
