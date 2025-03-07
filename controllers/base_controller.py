class Controller:
    def __init__(self, supabase_client, table):
        self.supabase = supabase_client
        self.table = table

    def validate_exist(self, value, v_name):
        exist = self.supabase.table(self.table).select(
            f"{v_name}").eq(v_name, value).execute()
        if not exist.data:
            message = f"El elemento con {v_name}: {value} no fue encontrado."
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
        return [model.from_dict(item) for item in response.data]

    def get_by_id_party(self, id_party, model):
        response = self.supabase.table(self.table).select(
            "*").eq("id_party", id_party).execute()
        return [model.from_dict(item) for item in response.data] if response.data else []

    def get_by_known_as(self, identifier, ide_name, model):
        if isinstance(identifier, str) and ide_name != "id":
            identifier = identifier.upper()

        exist, message = self.validate_exist(identifier, ide_name)
        if not exist:
            print(message)
            return None

        response = self.supabase.table(
            self.table).select("*").eq(ide_name, identifier).execute()
        return model.from_dict(response.data[0]) if response.data else None
