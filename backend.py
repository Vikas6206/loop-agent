import os
from typing import Literal, TypedDict

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import START,END,StateGraph
from pydantic import BaseModel, Field

load_dotenv()

MODEL = os.getenv("GROQ_MODEL","openai/gpt-oss-120b")
MAX_REVISIONS = int(os.getenv("MAX_REVISIONS", "2"))

model = ChatGroq(
    model=MODEL,
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)


## PYDANTIC class - It is used to generate the structured output for the reviewer.

class Review(BaseModel):
    decision: Literal["PASS", "REVISE"] = Field(
        description="PASS only if answer satisfy every review rule; otherwise REVISE"
    )
    feedback: str = Field(
        description=" Short, specific feedback. Empty string when decision is PASS."
    )

reviewer_model = model.with_structured_output(Review)


## State memory from langgraph [TypeDict - Type as dictionary]

class State(TypedDict):
    topic:str
    draft:str
    feedback:str
    decision:str
    revision_count:int


## WRITER AGENT
def writer(state: State):
    """ Agent 1: create the first answer."""
    response = model.invoke(
      [
            {
                "role": "system",
                "content": (
                    "You are a beginner-friendly teacher. Explain the topic in 120-160 words. "
                    "Use simple language, one everyday analogy, and one tiny example."
                ),
            },
            {
                "role": "user",
                "content": f"Explain: {state['topic']}",
            },
      ]
    )

    return {
        "draft": response.content,
        "feedback":"",
        "decision":"",
        "revision_count":0,
    }


## REVIEWER AGENT

def reviewer(state: State):
    """Agent 2:  Evaluate the current answer."""
    review = reviewer_model.invoke(
        [
            {
                "role": "system",
                "content": (
                    "You  are a strict reviewer. Check answer using ONLY these rules:\n"
                    "1. Is is easy for beginner.\n"
                    "2. It contains an everyday analogy.\n"
                    "3. It contains a tiny concrete example.\n"
                    "4. It stays focused onthe requested topic.\n"
                    "If any rule fails, choose REVISE and give one or two precise improvements."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Topic: {state['topic']}\n"
                    f"Answer: {state['draft']}\n"
                ),
            },
        ]
    )

    return {
        "decision": review.decision,
        "feedback": review.feedback,
    }


## Now the deision can be PASS or REVISE

## REVISER AGENT

def reviser(state: State):
    """Agent 3: Revise the answer using the reviewer's feedback."""
    response = model.invoke(
        [
            {
                "role": "system",
                "content": (
                    "You are a careful reviser. Use the reviewer's feedback to improve the answer while keeping it focused on the requested topic. "
                    "Keep it beginner-friendly and concise. Return only the improved answer."
                   
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Topic: {state['topic']}\n"
                    f"Current answer: {state['draft']}\n"
                    f"Reviewers Feedback: {state['feedback']}\n"
                ),
            },
        ]
    )

    return {
        "draft": response.content,
        "revision_count": state["revision_count"] + 1,
    }

## Route after review 
def route_after_review(state: State):
    """The loop controller."""
    if state["decision"] == "PASS":
        return "done"
    if state["revision_count"] >= MAX_REVISIONS:
        return "done"
    return "revise"

## StateGraph - Nodes & Edges

builder = StateGraph(State)
builder.add_node("writer", writer)
builder.add_node("reviewer", reviewer)
builder.add_node("reviser", reviser)


builder.add_edge(START, "writer")
builder.add_edge("writer", "reviewer")


builder.add_conditional_edges(
    "reviewer",
    route_after_review,
    {"revise": "reviser", "done": END},
)

builder.add_edge("reviser", "reviewer")

graph = builder.compile()


def run_workflow(topic: str):
    """ Run the graph and return data that both the CLI & FastAPI UI can use."""

    initial_state:State = {
        "topic": topic,
        "draft": "",
        "feedback": "",
        "decision": "",
        "revision_count": 0,
    }

    final_state = initial_state.copy()
    events = []


    for update in graph.stream(initial_state, stream_mode="updates"):
        for node_name, values in update.items():
            final_state.update(values)
            events.append({
                "agent": node_name,
                "draft": values.get("draft", ""),
                "feedback": values.get("feedback", ""),
                "decision": values.get("decision", ""),
                "revision_count": final_state["revision_count"],
            })


    return {
        "topic":topic,
        "events":events,
        "final_answer": final_state["draft"],
        "final_decision": final_state["decision"],
        "final_revision_count": final_state["revision_count"],
        "provider":"Groq",
        "model": MODEL,
    }


def cli_main():
    import sys

    sys.stdout.reconfigure(encoding="utf-8")
    topic = " ".join(sys.argv[1:]) or "What is an API?"
    result = run_workflow(topic)
    for event in result["events"]:
        print(f"[{event['agent']}] decision={event['decision']!r} feedback={event['feedback']!r}")
    print(f"\nFinal ({result['final_decision']}, revisions={result['final_revision_count']}):\n")
    print(result["final_answer"])


if __name__ == "__main__":
    cli_main()
