import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import Party
from controllers import PartyController

if __name__ == "__main__":
    from supabase import create_client

    url = 'https://tpgbsatkplqmdglpiuyz.supabase.co/'
    key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwZ2JzYXRrcGxxbWRnbHBpdXl6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDEyODU1NzAsImV4cCI6MjA1Njg2MTU3MH0.EvTW2Ktpqtl3FANUTT7Q3z_v-oYQN1kU-83PnF0AvPo'
    supabase = create_client(url, key)
    party_controller = PartyController(supabase)

    # Prueba Obtener todos los partidos
    print("\n---- Listado de partidos ----")
    partidos = party_controller.get_all_parties()
    for partido in partidos:
        print(
            f"ID: {partido.id}, Nombre: {partido.name}, Siglas: {partido.acronym}, Fundacion: {partido.fundation_date}")

    # Prueba Obtener por id
    id = 1
    print(f"\nPartido por id: {id}")
    partido = party_controller.get_party_by_id(id)
    print(f"ID: {partido.id}, Nombre: {partido.name}, Siglas: {partido.acronym}")

    # Prueba Obtener por Nombre
    name = "Morena"
    print(f"\nPartido por nombre: {name}")
    partido = party_controller.get_party_by_name(name)
    if partido:
        print(
            f"ID: {partido.id}, Nombre: {partido.name}, Siglas: {partido.acronym}")
    else:
        print("Partido no encontrado.")

    # Obtener por Siglas
    acronym = "PAN" 
    print(f"\nPartido por siglas: {acronym}")
    partido = party_controller.get_party_by_acronym(acronym)
    if partido:  # Verifica si partido no es None
        print(
            f"ID: {partido.id}, Nombre: {partido.name}, Siglas: {partido.acronym}")
    else:
        print("Partido no encontrado.")

    print("\nCrear Party")
    new_party = Party(name="Partido Revolucionario Independiente",acronym="PRI",fundation_date="2000-03-12",ideology="Derecha")
    partido = party_controller.create_party(new_party)

    # update_party = Party(1,"Morena",None,"2015-02-10","Izquierda",None)
    #partido = party_controller.update_party(update_party)
    
    print("\nEliminar Partido")
    id = 2
    partido = party_controller.delete_party(id)
