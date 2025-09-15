PROMPT_TEMPLATE = """
Generate a vivid, realistic persona profile for a believable adult from a diverse background, following a structured flow to ensure coherent character development.

## Generation Flow

Follow this systematic approach using the provided foundation:
1. Start with the foundation characteristics as your base
2. Expand the age group into specific demographics and life context
3. Build education background and occupation that fit the personality
4. Develop the economic context in detail
5. Expand personality traits into specific behaviors, values, and interests
6. Create detailed communication and behavioral patterns that align

## Foundation-Based Development

Use the provided foundation characteristics to guide all decisions:
- **Age group**: Develop into specific life stage, circumstances, and context
- **Personality**: Expand into detailed traits, motivations, and behavioral patterns
- **Communication style**: Build into specific speech patterns with examples
- **Attitudes**: Develop into detailed expectations and interaction style
- **Economic context**: Flesh out into realistic financial situation and priorities

## Required Output Format

Provide a structured persona profile with these exact fields:

**Summary:** Brief descriptive label that captures their interaction style
Examples: "Detail-Oriented Analyst", "Impatient Decision Maker", "Cautious First-Timer"

**Demographics:**
- age_group: teen, young_adult, adult, or senior
- education: Educational background and qualifications
- occupation: Current job or profession
- economic_status: Economic status and financial situation

**Psychology:**
- personality_traits: Core characteristics in flowing description
- values: Fundamental principles they live by
- interests: Main passions or areas of expertise

**Communication:**
- speech_style: Overall approach to conversation and interaction
- speech_patterns: Specific patterns with examples from personality/background

**Behavior:**
- typical_behavior: How they act in social situations, work, and daily life
- stress_triggers: Situations that create tension for them
- stress_reactions: How they cope with or react to stress

## Quality Standards

**Authenticity Requirements:**
- All cultural, linguistic, and geographic details must align consistently
- Occupation should fit economic and educational context of background
- Interests and behaviors should reflect cultural background and personal circumstances
- Avoid stereotypes while maintaining cultural authenticity

**Diversity Requirements:**
- No two personas should share the same combination of location, age range, and occupation
- Ensure variety in personality types, economic backgrounds, and life situations
- Include people from smaller cities/towns, not just major metropolitan areas
- Represent different life stages and career phases within age ranges

**Realism Requirements:**
- All details should be plausible and interconnected
- Include specific, concrete details rather than generic traits
- Show how background influences current behavior and perspectives
- Speech patterns should emerge naturally from personality and background
- Allow for realistic incompleteness - some fields can be empty strings if unknown/unclear

**Communication Authenticity:**
- Speech style should reflect education, culture, age, and personality
- Speech patterns should include specific examples of how they talk
- Avoid artificial typing quirks - focus on natural communication tendencies
- Consider how stress, excitement, or comfort levels might affect their communication

## Examples

**Tyler Brooks, 22:**
Background: "Lives in Phoenix, Arizona, dropped out of community college after one semester, works at Amazon fulfillment center. Lives with roommates, works mandatory overtime while trying to save money. Frustrated with dead-end job prospects and mounting student debt."

Speech patterns: "Cuts people off mid-sentence ('Nah, that's bullshit'), uses extreme language ('literally the worst', 'absolutely insane'), references online culture ('that's some boomer logic')"

**Catherine Blackwell, 38:**
Background: "Lives in Edinburgh, Scotland, graduated from Oxford Law School, worked at top London firms before relocating to Edinburgh for better work-life balance. Senior legal counsel at an international consulting firm. Single mother to an 8-year-old daughter."

Speech patterns: "Structures responses in logical sequence ('First, let me address...'), uses conditional language to show nuance ('It would depend on several factors'), references legal frameworks even in casual conversation"

## Instructions

- Use the foundation characteristics as your starting point - do NOT randomly select
- Build a coherent persona where all elements reinforce the foundation traits
- Create a concise summary that captures their key interaction style based on the foundation
- Include specific, memorable details that bring the foundation personality to life
- Ensure all attributes align with and expand upon the foundation characteristics
- Generate speech patterns that emerge naturally from the foundation personality and communication style
- Output only the structured JSON profile - no process explanation

## Foundation Characteristics
Build upon this persona foundation to create a complete, detailed profile:

{{foundation}}
"""
