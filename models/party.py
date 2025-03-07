"""
Modelo que representa a un partido político en el sistema.
"""
from datetime import datetime


class Party:
    """
    Clase de un partido político.
    """

    def __init__(self, id=None, name=None, acronym=None, fundation_date=None, ideology=None,
                description=None):
        """
        Inicializa una nueva instancia de Partido.
        """
        self.id = id
        self.name = name
        self.acronym = acronym
        self.fundation_date = fundation_date
        self.ideology = ideology
        self.description = description

    def to_dict(self):
        """
        Convierte la instancia del partido a un diccionario.
        """
        fecha_formateada = None
        if self.fundation_date:
            if isinstance(self.fundation_date, datetime):
                fecha_formateada = self.fundation_date.strftime('%Y-%m-%d').date()
            else:
                fecha_formateada = self.fundation_date

        return {
            'name': self.name,
            'acronym': self.acronym,
            'fundation_date': fecha_formateada,
            'ideology': self.ideology,
            'description': self.description
        }

    @classmethod
    def from_dict(cls, data):
        """
        Convierte de diccionario a instancia.
        """
        fundation_date = data.get("fundation_date")
        if fundation_date and isinstance(fundation_date, str):
            try:
                fundation_date = datetime.strptime(fundation_date, '%Y-%m-%d').date()
            except ValueError:
                pass

        return cls(
            id=data.get("id"),
            name=data.get("name"),
            acronym=data.get("acronym"),
            fundation_date=fundation_date,
            ideology=data.get("ideology"),
            description=data.get("description")
        )
