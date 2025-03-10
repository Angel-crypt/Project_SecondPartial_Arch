class Controller:
    def __init__(self, supabase_client, table):
        self.supabase = supabase_client
        self.table = table

    def print_info(self, model):
        """
        Imprime la información del afiliado.
        """
        partido_name = self.get_name_party(
            model.id_party)
        if model.id_party is None:
            partido_name = "Sin partido"
        else:
            partido_name = self.get_name_party(model.id_party)

        print(
            f"ID: {model.id}, Nombre: {model.name}, "
            f"Número de documento: {model.id_card}, Partido: {partido_name}"
        )

    
    def print_all_info(self, model, alls):
        """
        Imprime la información de todos los afiliados.
        """
        if alls:
            for one in alls:
                self.print_info(one)
        else:
            print("No hay afiliados disponibles.")

    def validate_exist(self, value, v_name, searchable, table=None):
        if table is None:
            table = self.table

        exist = self.supabase.table(table).select(
            f"{v_name}").eq(v_name, value).execute()
        if not exist.data:
            message = f"El {searchable} con {v_name}: {value} no fue encontrado."
            return False, message
        return True, "Elemento encontrado."

    def get_name_party(self, party_id):
        from .party_controller import PartyController
        party_controller = PartyController(self.supabase)
        party = party_controller.get_party_by_id(party_id)
        if party:
            return party.name
        else:
            return "Partido no encontrado."

    def get_all(self, model):
        response = self.supabase.table(self.table).select("*").execute()
        if response.data: 
            return [model.from_dict(item) for item in response.data]
        else:
            print("No se encontraron registros.")
            return False

    def get_by_id_party(self, id_party, model):
        response = self.supabase.table(self.table).select(
            "*").eq("id_party", id_party).execute()
        if response.data:
            return [model.from_dict(item) for item in response.data] if response.data else []
        else:
            print(f"No hay afiliados en el partido {self.get_name_party(id_party)}")

    def get_by_known_as(self, identifier, ide_name, model, searchable):
        if isinstance(identifier, str) and ide_name != "id":
            identifier = identifier.upper()

        exist, message = self.validate_exist(identifier, ide_name, searchable)
        if not exist:
            print(message)
            return None

        response = self.supabase.table(
            self.table).select("*").eq(ide_name, identifier).execute()
        return model.from_dict(response.data[0]) if response.data else None
