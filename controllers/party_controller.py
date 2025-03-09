import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models import Party
from controllers import Controller

class PartyController(Controller):
    def __init__(self, supabase_client):
        super().__init__(supabase_client, "parties")

    def get_all_parties(self):
        return self.get_all(Party)

    def get_party_by_id(self, id):
        return self.get_by_known_as(id, "id", Party,"partido")

    def get_party_by_name(self, name):
        return self.get_by_known_as(name, "name", Party,"partido")

    def get_party_by_acronym(self, acronym):
        return self.get_by_known_as(acronym, "acronym", Party,"partido")

    def create_party(self, partido):
        partido.name = partido.name.upper()
        partido.acronym = partido.acronym.upper()
        try:
            response = self.supabase.table(self.table).insert(
                partido.to_dict()).execute()
            if response.data and len(response.data) > 0:
                print(f"Partido creado")
                partido.id = response.data[0]['id']
                # Devuelves el objeto partido y el código de estado 201 (Created)
                return partido, 201
            else:
                print(f"Error al crear partido")
                # Si no se pudo crear el partido, devuelve None y código 400 (Bad Request)
                return {'error': 'No se pudo crear el partido'}, 400
        except Exception as e:
            if hasattr(e, 'code') and e.code == '23505':
                print(f"El partido '{partido.name}' ya existe.")
                # Si el partido ya existe, devuelve un error con código 409 (Conflict)
                return {'error': f"El partido '{partido.name}' ya existe."}, 409
            else:
                print(f"Error al crear partido: {e}")
                # Si ocurrió otro tipo de error, devuelve el error con código 500 (Internal Server Error)
                return {'error': f"Error al crear partido: {e}"}, 500
        
    def update_party(self, partido):
        # Verificar si el partido existe
        exist, message = self.validate_exist(partido.id, "id", "partido")
        if not exist:
            print(message)
            # Si no existe, devuelve un mensaje de error y el código 404 (Not Found)
            return {'error': 'Partido no encontrado'}, 404

        partido.name = partido.name.upper()
        partido.acronym = partido.acronym.upper()

        try:
            response = self.supabase.table(self.table).update(
                partido.to_dict()).eq("id", partido.id).execute()

            if response.data and len(response.data) > 0:
                print(
                    f'Informacion del partido "{partido.name}" actualizada correctamente')
                partido.id = response.data[0]['id']
                # Devuelve el partido actualizado y el código 200 (OK)
                return partido, 200
            else:
                print(f"Error al actualizar partido")
                # Si no se pudo actualizar el partido, devuelve el error con código 400
                return {'error': 'No se pudo actualizar el partido'}, 400
        except Exception as e:
            print(f"Error al actualizar partido: {e}")
            # Si ocurre un error inesperado, devuelve el error con código 500 (Internal Server Error)
            return {'error': f"Error al actualizar partido: {e}"}, 500

    def check_affiliates_or_representatives(self, party_id):
        """
        Verifica si un partido tiene afiliados o representantes.
        Retorna una tupla (tiene_afiliados, tiene_representantes).
        """
        try:
            # Verificar si hay representantes asociados al partido
            representatives = self.supabase.table("representatives").select(
                "id").eq("id_party", party_id).execute()
            has_representatives = len(representatives.data) > 0

            # Verificar si hay afiliados asociados al partido
            affiliates = self.supabase.table("affiliates").select(
                "id").eq("id_party", party_id).execute()
            has_affiliates = len(affiliates.data) > 0

            return has_affiliates, has_representatives
        except Exception as e:
            print(f"Error al verificar afiliados o representantes: {e}")
            return False, False


    def delete_party(self, id, confirm_deletion=False):
        """
        Elimina un partido de la base de datos.
        Si el partido tiene representantes o afiliados, devuelve un mensaje pidiendo confirmación.
        Si el cliente confirma, se elimina el partido.
        """
        # Verificar si el partido existe
        exist = self.supabase.table("parties").select(
            "id").eq("id", id).execute()
        if not exist.data:
            print(f"El partido con id: {id} no fue encontrado.")
            return False, "Partido no encontrado."

        # Verificar si hay afiliados o representantes
        has_affiliates, has_representatives = self.check_affiliates_or_representatives(
            id)

        # Si tiene afiliados o representantes, no eliminar directamente
        if has_representatives or has_affiliates:
            if confirm_deletion:
                    # Realizar la eliminación ya que se confirmó
                try:
                    self.supabase.table("representatives").update(
                        {"id_party": None}).eq("id_party", id).execute()
                    self.supabase.table("affiliates").update(
                        {"id_party": None}).eq("id_party", id).execute()
                    response = self.supabase.table(
                        "parties").delete().eq("id", id).execute()
                    if response.data:
                        return True, f"El partido con id: {id} ha sido eliminado exitosamente."
                    else:
                        return False, "No se pudo eliminar el partido."
                except Exception as e:
                    return False, f"Error al eliminar el partido: {e}"
            else:
                # Si no se confirma, devolver el mensaje de requerimiento de confirmación
                return False, "Este partido tiene afiliados o representantes. Se requiere confirmación para eliminarlo."

        try:
            # Eliminar el partido directamente si no tiene afiliados ni representantes
            response = self.supabase.table(
                "parties").delete().eq("id", id).execute()
            if response.data and len(response.data) > 0:
                print(f"Partido con id: {id} eliminado correctamente.")
                return True, "Partido eliminado correctamente."
            else:
                print(f"No se pudo eliminar el partido con id: {id}.")
                return False, "No se pudo eliminar el partido."
        except Exception as e:
            print(f"Error al eliminar partido: {e}")
            return False, f"Error al eliminar partido: {e}"
