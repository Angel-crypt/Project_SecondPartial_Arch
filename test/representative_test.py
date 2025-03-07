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
    representantes = representative_controller.get_all_representatives()
    for representative in representantes:
        partido = representative_controller.get_name_party(representative.id_party)
        print(
            f"ID: {representative.id}, Nombre: {representative.name}, 'Numero de document':{representative.id_card}, 'Partido':{partido}")

    # Prueba Obtener por id
    id = 1
    print(f"\nRepresentante por id: {id}")
    representante = representative_controller.get_representative_by_id(id)
    partido = representative_controller.get_name_party(representante.id_party)
    if representante:
        print(
            f"ID: {representante.id}, Nombre: {representante.name}, 'Numero de document':{representante.id_card}, 'Partido':{partido}")
    else:
        print("Representa no encontrado.")

    # Prueba obtener por id de partido
    id_party = 1
    partido = representative_controller.get_name_party(id_party)
    print(f"\nRepresentante por Partido, id: {id_party} = {partido}")
    representantes = representative_controller.get_representative_by_party(
        id_party)
    if partido:
        if representantes:
            for representative in representantes:
                print(
                    f"ID: {representative.id}, Nombre: {representative.name}, 'Numero de document':{representative.id_card}")
        else:
            print("El partido no tiene representantes.")
    else:
        print("Partido no encontrado")
    
    # Prueba obtener por nombre
    name = "Angel Cruz"
    print(f"\nObtener representante por nombre: {name}")
    representante = representative_controller.get_representative_by_name(name)
    partido = representative_controller.get_name_party(representative.id)
    if representante:
        print(
            f"ID: {representante.id}, Nombre: {representante.name}, 'Numero de document':{representante.id_card}, 'Partido':{partido.name}")

    # Crear representante
    print("\n")
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
