from src.db.models import Persona
from src.types import PersonaDTO


def persona_model_to_dto(persona: Persona) -> PersonaDTO:
    return PersonaDTO(
        id=persona.id,
        approval_status=persona.approval_status,
        attributes=persona.attributes,
        created_at=persona.created_at,
        metadata=persona.metadata_,
        purpose=persona.purpose,
        seq_id=persona.seq_id,
        simulation_id=persona.simulation_id,
        story=persona.story,
        summary=persona.summary,
        updated_at=persona.updated_at,
    )
