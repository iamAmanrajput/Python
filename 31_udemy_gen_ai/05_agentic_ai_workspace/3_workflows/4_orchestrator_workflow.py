# Generate a detailed report using an Orchestrator-Worker workflow
# We want to generate a complete report using multiple AI workers.
# First, the orchestrator creates a plan and divides the report into sections.
# Then, each worker writes one section in parallel.
# Finally, the synthesizer combines all sections into one final report.

from langchain_ollama import ChatOllama
from typing_extensions import TypedDict
from typing import Annotated, List
import operator
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import Send


# Create the LLM that will generate the report content
llm = ChatOllama(model="qwen3.5:0.8b")


# Define the structure of one report section
class Section(BaseModel):
    name: str = Field(description="Name for this section of the report")
    description: str = Field(
        description="Brief overview of the main topics and concepts of the section"
    )


# Define the structure of the complete report plan
class Sections(BaseModel):
    sections: List[Section] = Field(
        description="List of sections that should be included in the report"
    )


# Make the LLM return output in the defined Sections structure
planner = llm.with_structured_output(Sections)


# Define the shared state used by the main graph
class State(TypedDict):
    topic: str  # Topic of the report
    sections: list[Section]  # Sections created by the orchestrator
    completed_sections: Annotated[
        list, operator.add
    ]  # Sections written by all workers
    final_report: str  # Final report containing all completed sections


# Define the state used by each worker
class WorkerState(TypedDict):
    section: Section  # Section assigned to this worker
    completed_sections: Annotated[
        list, operator.add
    ]  # Store the section written by the worker


# -------------------- ORCHESTRATOR --------------------

def orchestrator(state: State):
    """Creates a plan for the report."""

    # Ask the LLM to divide the report topic into multiple sections
    report_sections = planner.invoke(
        [
            SystemMessage(content="Generate a plan for the report."),
            HumanMessage(
                content=f"Here is the report topic: {state['topic']}"
            ),
        ]
    )

    # Save the generated sections in the graph state
    return {"sections": report_sections.sections}


# -------------------- WORKER --------------------

def llm_call(state: WorkerState):
    """Writes the content for one report section."""

    # Ask the LLM to write the assigned section
    section = llm.invoke(
        [
            SystemMessage(
                content=(
                    "Write a report section following the provided name and "
                    "description. Include no preamble for each section. "
                    "Use Markdown Formatting."
                )
            ),
            HumanMessage(
                content=(
                    f"Here is the section name: {state['section'].name} "
                    f"and description: {state['section'].description}"
                )
            ),
        ]
    )

    # The returned data is used to update the graph's main State.
    # The key name must exist in State.
    # For example, "completed_sections" updates State["completed_sections"].
    # If multiple workers return the same key, the reducer combines their results.
    # Add the generated section to the shared completed_sections list
    return {"completed_sections": [section.content]}


# -------------------- ASSIGN WORKERS --------------------

def assign_workers(state: State):
    """Creates one worker for each report section."""

    # Send each section to a separate worker.
    # All workers can write their sections in parallel.
    return [
        Send("llm_call", {"section": section})
        for section in state["sections"]
    ]


# -------------------- SYNTHESIZER --------------------

def synthesizer(state: State):
    """Combines all completed sections into the final report."""

    # Get all sections written by the workers
    completed_sections = state["completed_sections"]

    # Join all sections together with a separator
    completed_report_sections = "\n\n---\n\n".join(
        completed_sections
    )

    # Save the combined sections as the final report
    return {"final_report": completed_report_sections}


# -------------------- BUILD WORKFLOW --------------------

# Create the LangGraph workflow using the main State
orchestrator_worker_builder = StateGraph(State)


# Add all nodes to the graph
orchestrator_worker_builder.add_node("orchestrator", orchestrator)
orchestrator_worker_builder.add_node("llm_call", llm_call)
orchestrator_worker_builder.add_node("synthesizer", synthesizer)


# -------------------- CONNECT NODES --------------------

# Start the workflow with the orchestrator
orchestrator_worker_builder.add_edge(
    START, "orchestrator"
)


# After planning, create workers dynamically for each section
orchestrator_worker_builder.add_conditional_edges(
    "orchestrator",
    assign_workers,
    ["llm_call"]
)


# After workers finish, send their results to the synthesizer
orchestrator_worker_builder.add_edge(
    "llm_call", "synthesizer"
)


# End the workflow after the final report is created
orchestrator_worker_builder.add_edge(
    "synthesizer", END
)


# -------------------- COMPILE WORKFLOW --------------------

# Compile the graph so it can be executed
orchestrator_worker = orchestrator_worker_builder.compile()


# -------------------- RUN WORKFLOW --------------------

# Start the workflow with the report topic
state = orchestrator_worker.invoke(
    {"topic": "Create a report on Agentic AI RAGs"}
)

print(state["final_report"])





    #                 topic
    #                   │
    #                   ▼
    #           ┌──────────────┐
    #           │ ORCHESTRATOR │
    #           └──────┬───────┘
    #                  │
    #           Creates sections
    #                  │
    #       ┌──────────┼──────────┐
    #       ▼          ▼          ▼
    #    Worker 1   Worker 2   Worker 3
    #       │          │          │
    #       ▼          ▼          ▼
    #    Section 1  Section 2  Section 3
    #       └──────────┼──────────┘
    #                  ▼
    #           completed_sections
    #                  │
    #                  ▼
    #           ┌─────────────┐
    #           │ SYNTHESIZER │
    #           └──────┬──────┘
    #                  ▼
    #             final_report