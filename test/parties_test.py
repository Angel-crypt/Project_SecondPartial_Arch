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
    parties = party_controller.get_all_parties()
    for party in parties:
        print(
            f"ID: {party.id}, Nombre: {party.name}, Siglas: {party.acronym}, Fundacion: {party.fundation_date}")

    # Prueba Obtener por id
    id = 2 #! Error aqui
    print(f"\nPartido por id: {id}")
    party = party_controller.get_party_by_id(id)
    if party is not None:
        print(f"ID: {party.id}, Nombre: {party.name}, Siglas: {party.acronym}")

    # Prueba Obtener por Nombre
    name = "Morena"
    print(f"\nPartido por nombre: {name}")
    party = party_controller.get_party_by_name(name)
    if party:
        print(
            f"ID: {party.id}, Nombre: {party.name}, Siglas: {party.acronym}")

    # Obtener por Siglas
    acronym = "PAN" 
    print(f"\nPartido por siglas: {acronym}")
    party = party_controller.get_party_by_acronym(acronym)
    if party:  # Verifica si partido no es None
        print(
            f"ID: {party.id}, Nombre: {party.name}, Siglas: {party.acronym}")

    print("\nCrear Partido")
    new_party = Party(name="Partido Revolucionario Independiente",acronym="PRI",fundation_date="2000-03-12",ideology="Derecha")
    party = party_controller.create_party(new_party)

    # update_party = Party(1,"Morena",None,"2015-02-10","Izquierda",None)
    #partido = party_controller.update_party(update_party)
    
    print("\nEliminar Partido")
    id = 1
    party = party_controller.delete_party(id)
