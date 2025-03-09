import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import Affiliate
from controllers import AffiliateController

if __name__ == "__main__":
    from supabase import create_client

    url = 'https://tpgbsatkplqmdglpiuyz.supabase.co/'
    key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwZ2JzYXRrcGxxbWRnbHBpdXl6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDEyODU1NzAsImV4cCI6MjA1Njg2MTU3MH0.EvTW2Ktpqtl3FANUTT7Q3z_v-oYQN1kU-83PnF0AvPo'
    supabase = create_client(url, key)
    affiliate_controller = AffiliateController(supabase)
    
    # Obtener todos los afiliados
    print("\n----Listado de afiliados----")
    affiliates = affiliate_controller.get_all_affiliates()
    if affiliates:
        affiliate_controller.print_all_info(Affiliate)
    
    # Obtener por id
    id = 1
    print(f"\nAfiliado por id: {id}")
    affiliate = affiliate_controller.get_affiliate_by_id(id)
    if affiliate:
        affiliate_controller.print_info(affiliate)

    # Obtener por nombre
    name = 'Angel Cruz'
    print(f"\nAfiliado por nombre: {name}")
    affiliate = affiliate_controller.get_affiliate_by_name(name)
    if affiliate:
        affiliate_controller.print_info(affiliate)

    # Obtener por id de partido
    print(f"\nAfiliado por Partido")
    id_party = 1
    party = affiliate_controller.get_name_party(id_party)
    if party != "Partido no encontrado.":
        print(f"Partido = {party}")
        affiliates = affiliate_controller.get_affiliate_by_party(id_party)

        if affiliates: 
            affiliate_controller.print_all_info(Affiliate)

    '''# Crear nuevo afiliado
    print("\nCrear nuevo afiliado")
    new_affiliate = Affiliate(name="Angel Cruz", id_card="frgiuhbhjbg",birth_date="2000-03-12",enrollment_date="2025-03-6",id_party=1)
    affiliate = affiliate_controller.create_affiliate(new_affiliate)

    # Actualizar afiliado
    print("\nActualizar informacion")
    update_info = Affiliate(id=7, name="Angel Nahum", id_card="dfglkkujfbdvf", birth_date="2005-03-09", enrollment_date="2025-03-6", id_party=5)
    affiliate = affiliate_controller.update_affiliate(update_info)

    # Eliminar afiliado
    print("\nEliminar afiliado")
    id = 16
    affiliate = affiliate_controller.delete_affiliate(id)'''
