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
        party_exist, message = self.validate_exist(
            representative.id_party, 'id', 'partido', table='parties')
        if party_exist:
            try:
                response = self.supabase.table(self.table).insert(
                    representative.to_dict()).execute()
                print("Representante agregado al partido.")
                return response.data is not None and len(response.data) > 0
            except Exception as e:
                if hasattr(e, 'code') and e.code == '23505':
                    print(
                        f"El numero de identificacion {representative.id_card} de '{representative.name}' ya esta registrado en el partido. Verifique el dato.")
                else:
                    print(f"Error al agregar al representante: {e}")
                return False
        else:
            print(message)

    def update_representative(self, representative):
        exist, message = self.validate_exist(representative.id, "id","representante")
        if not exist:
            print(message)
            return False
        
        representative.name = representative.name.upper()
        party_exist, message = self.validate_exist(
            representative.id_party, 'id', 'partido', table='parties')
        if party_exist:
            try:
                response = self.supabase.table(self.table).update(
                    representative.to_dict()).eq("id", representative.id).execute()
                print(
                    f'Informacion del Representante "{representative.name}" atualizada correctamente')
                return response.data is not None and len(response.data) > 0
            except Exception as e:
                print(f"Error al actualizar Representante: {e}")
                return False
        else:
            print(message)

    def delete_representative(self, id):
        exist, message = self.validate_exist(id, "id","representante")
        if not exist:
            print(message)
            return False

        try:
            validation = input(
                f"Confirmas la eliminacion del representante con id: {id}, (si/no): ")
            validation = validation.lower()
            if validation == "si":
                response = self.supabase.table(
                    self.table).delete().eq("id", id).execute()
                if response.data is not None:
                    print(
                        f"Representante con id: {id} eliminado correctamente.")
                    return True
                else:
                    print(
                        f"No se pudo eliminar el representante con id: {id}.")
                    return False
            else:
                print("Eliminación cancelada.")
                return False

        except Exception as e:
            print(f"Error al eliminar al representante: {e}")
            return False
