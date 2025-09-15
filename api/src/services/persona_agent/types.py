from pydantic import BaseModel

from src.types.simulations.personas import PersonaAttributesDTO


class PersonaGeneration(BaseModel):
    """
    Result of persona generation containing both summary and attributes
    """

    summary: str
    """
    Brief descriptive label for the persona's interaction style
    """

    attributes: PersonaAttributesDTO
    """
    Detailed persona attributes without summary field
    """
