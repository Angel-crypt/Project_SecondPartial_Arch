import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import Representative
from controllers import Controller

class RepresentativeController(Controller):
    def __init__(self, supabase_client):
        super().__init__(supabase_client, "representatives")
    
    def get_all_representatives(self):
        return self.get_all(Representative)

    def get_representative_by_id(self, id):
        return self.get_by_known_as(id, "id", Representative,"representante")

    def get_representative_by_name(self, name):
        return self.get_by_known_as(name, "name", Representative,"representante")
    
    def get_representative_by_party(self, id_party):
        return self.get_by_id_party(id_party, Representative)

    def create_representative(self, representative):
        representative.name = representative.name.upper()
        if representative.id_party is None or representative.id_party == 'None':
            representative.id_party = 0
        
        if representative.party_position is None or representative.party_position == 'None':
            representative.party_position = "Sin cargo"
        
        party_exist, message = self.validate_exist(
            representative.id_party, 'id', 'partido', table='parties')
        
        if party_exist:
            try:
                response = self.supabase.table(self.table).insert(
                    representative.to_dict()).execute()
                
                if response.data and len(response.data) > 0:
                    representative.id = response.data[0]['id']
                    return representative, 201
                else:
                    return {'error': 'No se pudo crear el representante'}, 400
                
            except Exception as e:
                if hasattr(e, 'code') and e.code == '23505':
                    return {'error': f"El número de identificación {representative.id_card} de '{representative.name}' ya está registrado."}, 409
                else:
                    return {'error': f"Error al agregar al afiliado: {e}"}, 500
        else:
            return {'error': message}, 404

    def update_representative(self, representative):
            # Verificar si el representante existe
        exist, message = self.validate_exist(
            representative.id, "id", "representante")
        if not exist:
            return {'error': 'Representante no encontrado'}, 404

        # Obtener el representante existente de la base de datos
        existing_representative_response = self.supabase.table(
            self.table).select('*').eq('id', representative.id).execute()

        if not existing_representative_response.data:
            return {'error': 'Representante no encontrado en la base de datos'}, 404

        # Obtener el primer (y único) representante
        existing_representative = existing_representative_response.data[0]

        # Actualizar solo los campos que se proporcionan en la solicitud
        representative.name = representative.name.upper(
        ) if representative.name else existing_representative['name']
        representative.id_card = representative.id_card if representative.id_card else existing_representative[
            'id_card']
        representative.birth_date = representative.birth_date if representative.birth_date else existing_representative[
            'birth_date']
        representative.enrollment_date = representative.enrollment_date if representative.enrollment_date else existing_representative[
            'enrollment_date']
        representative.id_party = representative.id_party if representative.id_party is not None else existing_representative[
            'id_party']
        representative.party_position = representative.party_position if representative.party_position else existing_representative[
            'party_position']

        # Validar si el partido existe
        party_exist, message = self.validate_exist(
            representative.id_party, 'id', 'partido', table='parties')
        if not party_exist:
            return {'error': message}, 404

        try:
            # Intentar actualizar el representante en la tabla
            response = self.supabase.table(self.table).update(
                representative.to_dict()).eq("id", representative.id).execute()

            if response.data and len(response.data) > 0:
                return representative, 200
            else:
                # Bad Request
                return {'error': 'No se pudo actualizar el representante'}, 400
        except Exception as e:
            # Internal Server Error
            return {'error': f"Error al actualizar representante: {e}"}, 500

    def delete_representative(self, id, confirm_deletion=False):
        exist = self.validate_exist(id, "id","representante")
        if not exist:
            return False, "Rrepesentante no encontrado."

        # Si confirm_deletion es False, devolver un mensaje de error
        if not confirm_deletion:
            return False, "Se requiere confirmación para eliminar el representante."

        try:
            # Intentar eliminar el representante de la tabla
            response = self.supabase.table(
                self.table).delete().eq("id", id).execute()
            if response.data and len(response.data) > 0:
                return True, f"Representante con id: {id} eliminado correctamente."
            else:
                return False, "No se pudo eliminar al representante."
        except Exception as e:
            return False, f"Error al eliminar al representante: {e}"
