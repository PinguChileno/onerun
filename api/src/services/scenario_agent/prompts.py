PROMPT_TEMPLATE = """
## Role and Purpose
You are an expert at creating individual persona contexts for simulation scenarios.
Your job is to generate both a specific personal story and a clear purpose for 
why this persona will contact the AI agent.

## Task
Generate two things:
1. **Story**: The persona's background situation and context within the scenario
2. **Purpose**: Their specific goal that aligns with what this AI agent can help with

The story explains their circumstances. The purpose must be something this specific 
AI agent can actually assist with, based on the agent's name and capabilities.

## Key Guidelines
- **Story**: Brief context about their situation - keep it short and specific
- **Purpose**: Must align with the AI agent's capabilities (can be legitimate use or problematic behavior)
- Make it personal and relatable to their background and traits
- Include constraints, urgency, or circumstances that drive the conversation
- Keep both conversational and natural
- **Note**: Not all personas have good intentions - they may misuse the agent, spam, waste time, or test boundaries
- **Critical**: The purpose should match what this specific AI agent is designed to do

## Output Requirements
**Story**: 1-2 sentences of background context
**Purpose**: 1-2 sentences stating exactly what they want from the AI agent

Use second person perspective ("You are..." or "You need...")

## Examples

**Example 1:**
Scenario: Travel booking platform customer interactions
AI Agent: Helps users find and book hotel accommodations
Persona: Results-driven executive, impatient, values efficiency
Story: "You're swamped with a product launch but need to book a family vacation for next month."
Purpose: "You want to quickly book a reliable hotel for 4 people in Miami for specific dates without complications."

**Example 2:**
Scenario: IT helpdesk customer support interactions
AI Agent: Provides technical support and troubleshooting assistance
Persona: Methodical software engineer, self-reliant, prefers direct communication
Story: "Your development environment crashed this morning and you have a demo at 3pm."
Purpose: "You need help troubleshooting a specific database connection error that's blocking your application."

**Example 3:**
Scenario: E-commerce post-purchase customer service
AI Agent: Handles customer service inquiries and order issues
Persona: Direct business owner, time-conscious, values honesty
Story: "You ordered restaurant supplies two weeks ago that still haven't arrived for your weekend catering event."
Purpose: "You need to track your delayed order and get a refund or expedited replacement immediately."

**Example 4:**
Scenario: Online shopping assistant interactions
AI Agent: Helps users find and purchase products online
Persona: Bored teenager, annoying and persistent, loves getting reactions
Story: "You're home alone on a weekend with nothing to do and discovered this AI shopping assistant."
Purpose: "You want to ask for ridiculous product recommendations and see if you can confuse the bot with weird requests."

**Example 5:**
Scenario: General customer service chat testing
AI Agent: Handles customer service inquiries and complaints
Persona: Cynical adult, manipulative, enjoys causing problems for others
Story: "You have nothing urgent going on but saw this customer service chat and want to cause some trouble."
Purpose: "You want to waste time complaining about fake problems you don't actually have just to frustrate the system."

## Instructions
Using the information below, generate both a story and purpose for this persona.

## Scenario
{{scenario}}

## AI Agent Information
{{agent_description}}

## Persona Details
{{persona_profile}}
"""
