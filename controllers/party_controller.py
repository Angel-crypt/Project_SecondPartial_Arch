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
        return self.get_by_known_as(id, "id", Party)

    def get_party_by_name(self, name):
        return self.get_by_known_as(name, "name", Party)

    def get_party_by_acronym(self, acronym):
        return self.get_by_known_as(acronym, "acronym", Party)

    def create_party(self, partido):
        partido.name = partido.name.upper()
        partido.acronym = partido.acronym.upper()
        try:
            response = self.supabase.table(self.table).insert(partido.to_dict()).execute()
            print(f"Partido creado")
            return response.data is not None and len(response.data) > 0
        except Exception as e:
            if hasattr(e, 'code') and e.code == '23505':
                print(f"El partido '{partido.name}' ya existe.")
            else:
                print(f"Error al crear partido: {e}")
            return False
    
    def update_party(self, partido):
        partido.name = partido.name.upper()
        partido.acronym = partido.acronym.upper()
        try:
            response = self.supabase.table(self.table).update(
                partido.to_dict()).eq("id", partido.id).execute()
            '''if partido.id'''
            print(f'Informacion del partido "{partido.name}" atualizada correctamente')
            return response.data is not None and len(response.data) > 0
        except Exception as e:
            print(f"Error al actualizar partido: {e}")
            return False
    
    def delete_party(self, id):
        exist = self.supabase.table("parties").select("id").eq("id",id).execute()
        if not exist.data:
            print(f"El partido con id: {id} no fue encontrado.")
            return False
        
        def action():
            validation = input("Confirmas la eliminación (si/no): ")
            validation = validation.lower()
            if validation == "si":
                response = self.supabase.table(
                    self.table).delete().eq("id", id).execute()
                if response.data is not None:
                    print(f"Partido con id: {id} eliminado correctamente.")
                    return True
                else:
                    print(f"No se pudo eliminar el partido con id: {id}.")
                    return False
            else:
                print("Eliminación cancelada.")
                return False
        
        try:
            ''' # Primero verificar si hay representantes o afiliados asociados
            representantes = self.supabase.table("representantes").select(
                "id").eq("partido_id", id).execute()
            if representantes.data and len(representantes.data) > 0:
                print("\nEl partido tiene representantes.")
                action()
            else:
                return False

            afiliados = self.supabase.table("afiliados").select(
                "id").eq("partido_id", id).execute()
            if afiliados.data and len(afiliados.data) > 0:
                print("\nEl partido tiene afiliados.")
                action()
            else:
                return False'''

            action()

            
        except Exception as e:
            print(f"Error al eliminar partido: {e}")
            return False
