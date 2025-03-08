import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from controllers import RepresentativeController
from models import Representative

if __name__ == "__main__":
    from supabase import create_client

    url = 'https://tpgbsatkplqmdglpiuyz.supabase.co/'
    key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwZ2JzYXRrcGxxbWRnbHBpdXl6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDEyODU1NzAsImV4cCI6MjA1Njg2MTU3MH0.EvTW2Ktpqtl3FANUTT7Q3z_v-oYQN1kU-83PnF0AvPo'
    supabase = create_client(url, key)
    representative_controller = RepresentativeController(supabase)

    # Prueba Obtener todos los representantes
    print("\n---- Listado de representantes ----")
    representatives = representative_controller.get_all_representatives()
    if representatives:
        representative_controller.print_all_info(Representative)

    # Prueba Obtener por id
    id = 2
    print(f"\nRepresentante por id: {id}")
    representative = representative_controller.get_representative_by_id(id)
    if representative:
        representative_controller.print_info(representative)

    # Prueba obtener por id de partido
    print(f"\nRepresentante por Partido")
    id_party = 2
    party = representative_controller.get_name_party(id_party)
    if party != "Partido no encontrado.":
        print(f"\nPartido = {party}")
        representatives = representative_controller.get_affiliate_by_party(id_party)

        if representatives:
            representative_controller.print_all_info(Representative)
    
    
    # Prueba obtener por nombre
    name = "Angel Cruz"
    print(f"\nObtener representante por nombre: {name}")
    representative = representative_controller.get_representative_by_name(name)
    if representative:
        representative_controller.print_info(representative)

    # Crear representante
    print("\nCrear nuevo representante")
    new_representative = Representative(name="Angel Cruz",id_card="frgiuhbhjbg",birth_date="2000-03-12",enrollment_date="2025-03-6",id_party=5)
    representante = representative_controller.create_representative(
        new_representative)
    
    # Actualizar representante
    print("\nActualizar informacion")
    update_info = Representative(id=2, name="Angel Cruz", id_card="dfglkkujfbdvf", birth_date="2005-03-09", enrollment_date="2025-03-6", id_party=5)
    representante = representative_controller.update_representative(update_info)
    
    # Eliminar representante
    print("\nEliminar representante")
    id = 3
    representante = representative_controller.delete_representative(id)
