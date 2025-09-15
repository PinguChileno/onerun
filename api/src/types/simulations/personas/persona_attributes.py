from pydantic import BaseModel, Field


class PersonaAttributesDTO(BaseModel):
    """
    Persona attributes with flexible completeness - empty strings indicate
    unknown/unclear aspects
    """

    # Demographics
    age_group: str = Field(
        description="Age group category",
        pattern="^(teen|young_adult|adult|senior)$"
    )
    """
    Age group: teen (13-19), young_adult (20-35), adult (36-55), senior (55+)
    """

    # Background
    education: str = Field(
        default="",
        description="Educational background and qualifications",
    )
    """
    Educational background and qualifications
    """
    occupation: str = Field(
        default="",
        description="Current job or profession",
    )
    """
    Current job or profession
    """
    economic_status: str = Field(
        default="",
        description="Economic status and financial situation",
    )
    """
    Economic status and financial situation
    """

    # Psychology
    personality_traits: str = Field(
        default="",
        description="Core characteristics in flowing description",
    )
    """
    Core characteristics in flowing description
    """
    values: str = Field(
        default="",
        description="Fundamental principles they live by",
    )
    """
    Fundamental principles they live by
    """
    habits: str = Field(
        default="",
        description="Specific behavioral patterns that reveal character",
    )
    """
    Specific behavioral patterns that reveal character
    """
    interests: str = Field(
        default="", description="Main passions or areas of expertise"
    )
    """
    Main passions or areas of expertise
    """
    # Communication
    speech_style: str = Field(
        description="Overall approach to conversation and interaction"
    )
    """
    Overall approach to conversation and interaction
    """
    speech_patterns: str = Field(
        default="",
        description=(
            "Specific patterns that emerge from their personality/background, "
            "with examples"
        ),
    )
    """
    Specific patterns that emerge from their personality/background, with
    examples
    """

    # Behavior
    typical_behavior: str = Field(
        default="",
        description=(
            "How they generally act in social situations, work, and daily life"
        ),
    )
    """
    How they generally act in social situations, work, and daily life
    """
    stress_triggers: str = Field(
        default="",
        description="Situations that create tension for them",
    )
    """
    Situations that create tension for them
    """
    stress_reactions: str = Field(
        default="",
        description="How they cope with or react to stress",
    )
    """
    How they cope with or react to stress
    """

    version: str = "1"
    """
    Schema version of the attributes
    """
