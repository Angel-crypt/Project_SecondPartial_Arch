import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import Affiliate
from controllers import Controller

class AffiliateController(Controller):
    def __init__(self, supabase_client):
        super().__init__(supabase_client, "affiliates")
    
    def get_affiliate_name_party(self, affiliate_id):
        affiliate = self.get_affiliate_by_id(affiliate_id)
        if not affiliate:
            return "Afiliado no encontrado"
        
        party_id = affiliate.id_party
        return self.get_name_party(party_id)
    
    def get_all_affiliates(self):
        return self.get_all(Affiliate)
    
    def get_affiliate_by_id(self, id):
        return self.get_by_known_as(id, "id", Affiliate)
    
    def get_affiliate_by_name(self, name):
        return self.get_by_known_as(name, "name", Affiliate)
    
    def get_affiliate_by_party(self, id_party):
        return self.get_by_id_party(id_party, Affiliate)
    
    def create_affiliate(self, affiliate):
        affiliate.name = affiliate.name.upper()
        try:
            reponse = self.supabase.table(self.table).insert(
                affiliate.to_dict()).execute()
            print("Afiliado agregado al partido.")
            return reponse.data is not None and len(reponse.data) > 0
        except Exception as e:
            if hasattr(e, 'code') and e.code == '23505':
                print(
                    f"El numero de identificacion {affiliate.id_card} de '{affiliate.name}' ya esta registrado en el partido. Verifique el dato.")
            else:
                print(f"Error al agregar al afiliado: {e}")
            return False
    
    def update_affiliate(self, affiliate):
        exist, messag = self.validate_exist(affiliate.id, "id")
        if not exist:
            print(messag)
            return False

        affiliate.name = affiliate.name.upper()
        try:
            response = self.supabase.table(self.table).update(
                affiliate.to_dict()).eq("id", affiliate.id).execute()
            print(f"Informacion del Afiliado '{affiliate.name}' actualizada correctamente.")
            return response.data is not None and len(response.data) > 0
        except Exception as e:
            print(f"Error al actualizar la informacion del afiliado: {e}")
            return False
    
    def delete_affiliate(self, id):
        exist, messag = self.validate_exist(id, "id")
        if not exist:
            print(messag)
            return False
        
        try:
            validation = input(f"Confirmas la eliminacion del afiliado con id: {id}, (si/no): ")
            validation = validation.lower()
            if validation == "si":
                reponse = self.supabase.table(self.table).delete().eq("id", id).execute()
                if reponse.data is not None:
                    print(f"Se ha eliminado correctamente el afiliado con id: {id}")
                    return True
                else:
                    print(f"No se pudo eliminar al afiliado con id: {id}")
                    return False
            else:
                print("Eliminacion cancelada.")
                return False
        
        except Exception as e:
            print(f"Error al eliminar al afilaido: {e}")
            return False
