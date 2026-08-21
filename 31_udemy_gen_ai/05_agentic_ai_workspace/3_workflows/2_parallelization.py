# example of parallelization workflow

import os
from dotenv import load_dotenv

load_dotenv()

from langchain_ollama import ChatOllama
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

llm = ChatOllama(model="gemma3:latest")

# Graph state
class State(TypedDict):
    topic: str
    characters: str
    settings: str
    premises: str
    story_intro: str

# Nodes
def generate_characters(state: State):
    """Generate character descriptions"""
    msg = llm.invoke(
        f"Create two character names and brief traits for a story about {state['topic']}"
    )
    return {"characters": msg.content}

def generate_setting(state: State):
    """Generate a story setting"""
    msg = llm.invoke(f"Describe a vivid setting for a story about {state['topic']}")
    return {"settings": msg.content}


def generate_premise(state: State):
    """Generate a story premise"""
    msg = llm.invoke(f"Write a one-sentence plot premise for a story about {state['topic']}")
    return {"premises": msg.content}

def combine_elements(state: State):
    """Combine characters, setting, and premise into an intro"""
    msg = llm.invoke(
        f"Write a short story introduction using these elements:\n"
        f"Characters: {state['characters']}\n"
        f"Setting: {state['settings']}\n"
        f"Premise: {state['premises']}"
    )
    return {"story_intro": msg.content}

# Build the graph
graph = StateGraph(State)

graph.add_node("character", generate_characters)
graph.add_node("setting", generate_setting)
graph.add_node("premise", generate_premise)
graph.add_node("combine", combine_elements)

# Define edges (parallel execution from START)
graph.add_edge(START, "character")
graph.add_edge(START, "setting")
graph.add_edge(START, "premise")
graph.add_edge("character", "combine")
graph.add_edge("setting", "combine")
graph.add_edge("premise", "combine")
graph.add_edge("combine", END)

# Compile and run
compiled_graph = graph.compile()

state = {"topic": "time travel"}
result = compiled_graph.invoke(state)
print(result["story_intro"])

# Okay, this is fantastic! The detail is incredible, and the characters are intriguing. Let’s craft a story introduction building on this rich foundation.

# ---

# The rain hammered against the stained-glass windows of the Core Chamber, a relentless, mournful rhythm that mirrored the frantic beat of Elias Vance’s heart. October 27th, 1888. Blackwood Institute. The air, thick with ozone and the unsettling tang of something like bruised lavender, clung to him like a shroud. He adjusted his spectacles, the brass frames cold against his skin, meticulously noting the slight misalignment of the main chronometer – a deviation of .003 degrees, a potentially catastrophic error in the delicate dance of temporal mechanics.

# “Damn it,” he muttered, his voice swallowed by the grinding whine of the Chronarium. The machine, a monstrous tangle of copper, crystal, and rusted gears, pulsed with an erratic, sickly green light. It was a beautiful horror, a testament to Alistair Blackwood’s obsessive genius – and his blatant disregard for safety.

# A sharp, insistent voice cut through the rhythmic drone. "You still fussing with the regulator, Professor? Time's a river, you know. Best let it flow."

# Elias turned to find Sera Reyes leaning against a column of blackened iron, a wrench dangling from her hand. She was a chaotic splash of scarlet leather and grease-stained denim amidst the Victorian decay. Her dark hair was pulled back in a practical braid, and her eyes, the color of polished steel, assessed him with a frank, unnerving directness. She looked utterly out of place, a punk rock insurgent in a mausoleum of temporal ambition.

# “Ms. Reyes,” Elias began, his voice tight with controlled irritation, “precision is paramount. This isn’t a workshop; it’s a…a temporal anomaly containment device.” 

# Sera snorted, kicking at a loose piece of brick. "Containment? Looks more like a glorified hamster wheel to me. And you’re wasting time arguing with yourself. The echoes are getting worse. I’m picking up significant temporal bleed – we need to stabilize the core before the whole thing collapses in on itself."

# Suddenly, the air shimmered. A brief, horrifying flash – a Roman legionary, clad in gleaming bronze armor, materialized for a heartbeat before dissolving back into the gloom, followed by the fleeting image of a flapper in a shimmering beaded dress. Elias instinctively reached for the emergency temporal dampener on his wrist, a device he’d designed himself, a fragile buffer against the instabilities he'd foreseen. 

# "Did you see that?" Sera asked, her voice low and urgent. “That’s not just an echo, Professor. That's a consequence. You’ve changed something. I’m detecting… dissonance.”

# Elias’s meticulous composure shattered. He stared at the Chronarium, at the pulsating green light, at the unsettling distortions in the air. The personal loss that had driven him – the death of his younger sister, Clara, a tragedy he’d spent decades desperately trying to understand, to *correct* – suddenly seemed impossibly complex, interwoven with the chaotic currents of time itself. He gripped his wrench, his knuckles white. "Show me," he said, his voice barely a whisper. “Show me what you've found."

# ---

# **Notes on this introduction:**

# *   **Show, Don't Tell:** I’ve tried to *show* Elias’s obsessive nature through his detailed observations and frustration, and Sera’s practical, instinctive approach through her actions and dialogue.
# *   **Character Dynamics:** The introduction establishes a clear dynamic between the two characters – Elias, the cautious scholar, and Sera, the impulsive inventor – with a sense of underlying tension and mutual respect.
# *   **Atmosphere and Mystery:** The description of the setting is woven throughout, emphasizing the unsettling and dangerous nature of the Chronarium and the potential consequences of their actions. The temporal echoes are introduced as a concrete element of the story’s premise.
# *   **Raising the Stakes:** The introduction ends with a heightened sense of urgency, suggesting that Elias’s attempt to prevent the past is already creating unforeseen and potentially disastrous consequences.


# To help me develop this further, could you tell me:

# *   What specifically caused Elias’s sister’s death? (Just a brief idea – was it an accident, a crime, a deliberate act?)
# *   Do you envision Elias and Sera working together collaboratively, or is there inherent conflict between their approaches?
# *   Are there any specific “rules” governing time travel within this universe? (e.g., limitations on the number of changes they can make, potential paradoxes, etc.)