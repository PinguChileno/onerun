import random


# Age groups - core demographic foundation
AGE_GROUPS = [
    "teen",          # 13-19
    "young_adult",   # 20-35
    "adult",         # 36-55
    "senior",        # 55+
]

# Personality traits - mix of normal and challenging characteristics
PERSONALITY_TRAITS = [
    "analytical and methodical",
    "creative and spontaneous",
    "nurturing and helpful",
    "ambitious and competitive",
    "practical and efficient",
    "optimistic and energetic",
    "cautious and thoughtful",
    "independent and self-reliant",
    "social and outgoing",
    "quiet and reflective",
    "perfectionist and organized",
    "relaxed and adaptable",
    "skeptical and questioning",
    "traditional and stable",
    "innovative and forward-thinking",
    "direct and blunt",
    "diplomatic and tactful",
    "impatient and results-focused",
    "patient and persistent",
    "emotional and expressive",
    "angry and confrontational",
    "aggressive and pushy",
    "annoying and persistent",
    "rude and dismissive",
    "entitled and demanding",
    "paranoid and suspicious",
    "arrogant and condescending",
    "passive-aggressive and sarcastic",
    "volatile and unpredictable",
    "stubborn and argumentative",
    "nitpicky and fault-finding",
    "dramatic and attention-seeking",
    "cynical and negative",
    "impatient and explosive",
    "manipulative and guilt-tripping",
]

# Communication styles - mix of normal and difficult patterns
COMMUNICATION_STYLES = [
    "gets straight to the point",
    "loves to chat and tell stories",
    "formal and professional",
    "casual and friendly",
    "enthusiastic and animated",
    "measured and careful",
    "confident and assertive",
    "avoids conflict",
    "uses humor frequently",
    "serious and focused",
    "asks lots of questions",
    "keeps things brief",
    "very expressive",
    "logical and structured",
    "rambles and goes off-topic",
    "interrupts constantly",
    "talks over everyone",
    "never listens to answers",
    "complains about everything",
    "makes unreasonable demands",
    "threatens and intimidates",
    "uses insults and name-calling",
    "guilt-trips and manipulates",
    "yells and shouts",
    "hangs up or storms off",
    "refuses to explain what they want",
    "changes their story constantly",
    "blames everyone else",
    "makes personal attacks",
]

# Attitudes and expectations
ATTITUDES = [
    "expects high quality service",
    "doesn't like to spend much money",
    "wants everything explained clearly",
    "gets impatient with delays",
    "very price-conscious",
    "values convenience above all",
    "expects personal attention",
    "likes to research everything first",
    "trusts recommendations easily",
    "skeptical of sales pitches",
    "wants the latest and greatest",
    "prefers tried and true options",
    "expects things to be free or cheap",
    "willing to pay for quality",
    "hates being rushed",
    "wants quick decisions",
    "needs lots of reassurance",
    "very decisive and confident",
]

# Economic context
ECONOMIC_STATUS = [
    "tight budget",
    "comfortable financially",
    "very wealthy",
    "struggling with money",
    "price doesn't matter",
    "looks for deals",
    "spends carefully",
    "impulse buyer",
]


def generate_foundation() -> str:
    """
    Generate a simple persona foundation for AI to expand.

    Returns basic characteristics like:
    "Teen, impatient and results-focused, gets straight to the point, 
     expects things to be free, tight budget"
    """
    age = random.choice(AGE_GROUPS)
    personality = random.choice(PERSONALITY_TRAITS)
    communication = random.choice(COMMUNICATION_STYLES)
    attitude = random.choice(ATTITUDES)
    economic = random.choice(ECONOMIC_STATUS)

    return (
        f"{age}, {personality}, {communication}, "
        f"{attitude}, {economic}"
    )
