"""
Modelo que representa a un representante político en el sistema.
"""
from datetime import datetime


class Representative:
    """
    Clase de un representante político.
    """

    def __init__(self, id=None, name=None, id_card=None, birth_date=None, enrollment_date=None, id_party=None, party_position=None):
        """
        Inicializa una nueva instancia de Representante.
        """
        self.id = id
        self.name = name
        self.id_card = id_card
        self.birth_date = birth_date
        self.enrollment_date = enrollment_date
        self.id_party = id_party
        self.party_position = party_position

    def to_dict(self):
        """
        Convierte la instancia del representante a un diccionario.
        """
        birth_date_formatted = None
        if self.birth_date:
            if isinstance(self.birth_date, datetime):
                birth_date_formatted = self.birth_date.strftime('%Y-%m-%d').date()
            else:
                birth_date_formatted = self.birth_date

        enrollment_date_formatted = None
        if self.enrollment_date:
            if isinstance(self.enrollment_date, datetime):
                enrollment_date_formatted = self.enrollment_date.strftime(
                    '%Y-%m-%d').date()
            else:
                enrollment_date_formatted = self.enrollment_date

        return {
            'name': self.name,
            'id_card': self.id_card,
            'birth_date': birth_date_formatted,
            'enrollment_date': enrollment_date_formatted,
            'id_party': self.id_party,
            'party_position': self.party_position
        }

    @classmethod
    def from_dict(cls, data):
        """
        Convierte de diccionario a instancia.
        """
        birth_date = data.get("birth_date")
        if birth_date and isinstance(birth_date, str):
            try:
                birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
            except ValueError:
                pass

        enrollment_date = data.get("enrollment_date")
        if enrollment_date and isinstance(enrollment_date, str):
            try:
                enrollment_date = datetime.strptime(
                    enrollment_date, '%Y-%m-%d').date()
            except ValueError:
                pass

        return cls(
            id=data.get("id"),
            name=data.get("name"),
            id_card=data.get("id_card"),
            birth_date=birth_date,
            enrollment_date=enrollment_date,
            id_party=data.get("id_party"),
            party_position=data.get("party_position")
        )
