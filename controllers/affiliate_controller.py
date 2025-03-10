import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import Affiliate
from controllers import Controller

class AffiliateController(Controller):
    def __init__(self, supabase_client):
        super().__init__(supabase_client, "affiliates")
    
    def get_all_affiliates(self):
        return self.get_all(Affiliate)
    
    def get_affiliate_by_id(self, id):
        return self.get_by_known_as(id, "id", Affiliate,"afiliado")
    
    def get_affiliate_by_name(self, name):
        return self.get_by_known_as(name, "name", Affiliate,"afiliado")
    
    def get_affiliate_by_party(self, id_party):
        return self.get_by_id_party(id_party, Affiliate)
    
    def create_affiliate(self, affiliate):
        affiliate.name = affiliate.name.upper()
        if affiliate.id_party is None or affiliate.id_party == 'None':
            affiliate.id_party = 0
        party_exist, message = self.validate_exist(
            affiliate.id_party, 'id', 'partido', table='parties')

        if party_exist:
            try:
                response = self.supabase.table(self.table).insert(
                    affiliate.to_dict()).execute()

                if response.data and len(response.data) > 0:
                    affiliate.id = response.data[0]['id']
                    return affiliate, 201
                else:
                    return {'error': 'No se pudo crear el afiliado'}, 400
            except Exception as e:
                if hasattr(e, 'code') and e.code == '23505':
                    # Conflict
                    return {'error': f"El número de identificación {affiliate.id_card} de '{affiliate.name}' ya está registrado."}, 409
                else:
                    # Internal Server Error
                    return {'error': f"Error al agregar al afiliado: {e}"}, 500
        else:
            return {'error': message}, 404  # Not Found
    
    def update_affiliate(self, affiliate):
        # Verificar si el afiliado existe
        exist, message = self.validate_exist(affiliate.id, "id", "afiliado")
        if not exist:
            # Devuelve un mensaje de error y código 404
            return {'error': 'Afiliado no encontrado'}, 404

        # Obtener el afiliado existente de la base de datos
        existing_affiliate_response = self.supabase.table(
            self.table).select('*').eq('id', affiliate.id).execute()

        if not existing_affiliate_response.data:
            return {'error': 'Afiliado no encontrado en la base de datos'}, 404

        # Obtener el primer (y único) afiliado
        existing_affiliate = existing_affiliate_response.data[0]

        # Actualizar solo los campos que se proporcionan en la solicitud
        affiliate.name = affiliate.name.upper(
        ) if affiliate.name else existing_affiliate['name']
        affiliate.id_card = affiliate.id_card if affiliate.id_card else existing_affiliate[
            'id_card']
        affiliate.birth_date = affiliate.birth_date if affiliate.birth_date else existing_affiliate[
            'birth_date']
        affiliate.enrollment_date = affiliate.enrollment_date if affiliate.enrollment_date else existing_affiliate[
            'enrollment_date']

        # Si no se proporciona un ID de partido, mantener el existente
        affiliate.id_party = affiliate.id_party if affiliate.id_party is not None else existing_affiliate[
            'id_party']

        # Validar si el partido existe
        party_exist, message = self.validate_exist(
            affiliate.id_party, 'id', 'partido', table='parties')

        if not party_exist:
            print(message)
            # Devuelve un mensaje de error y código 404
            return {'error': message}, 404

        try:
            # Intentar actualizar el afiliado en la tabla
            response = self.supabase.table(self.table).update(
                affiliate.to_dict()).eq("id", affiliate.id).execute()

            if response.data and len(response.data) > 0:
                # Devuelve el objeto afiliado actualizado y el código 200 (OK)
                return affiliate, 200
            else:
                # Bad Request
                return {'error': 'No se pudo actualizar el afiliado'}, 400
        except Exception as e:
            # Internal Server Error
            return {'error': f"Error al actualizar afiliado: {e}"}, 500
    
    def delete_affiliate(self, id, confirm_deletion=False):
        # Verificar si el afiliado existe
        exist, message = self.validate_exist(id, "id", "afiliado")
        if not exist:
            return False, "Afiliado no encontrado."

        # Si confirm_deletion es False, devolver un mensaje de error
        if not confirm_deletion:
            return False, "Se requiere confirmación para eliminar el afiliado."

        try:
            # Intentar eliminar el afiliado
            response = self.supabase.table(
                self.table).delete().eq("id", id).execute()
            if response.data and len(response.data) > 0:
                print(f"Se ha eliminado correctamente el afiliado con id: {id}")
                return True, f"Afiliado con id: {id} eliminado correctamente."
            else:
                print(f"No se pudo eliminar al afiliado con id: {id}")
                return False, "No se pudo eliminar al afiliado."
        except Exception as e:
            print(f"Error al eliminar al afiliado: {e}")
            return False, f"Error al eliminar al afiliado: {e}"
