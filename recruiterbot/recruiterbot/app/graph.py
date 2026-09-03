from typing import TypedDict, List
from langgraph.graph import StateGraph, END

from app.nodes.classify import classify_node
from app.nodes.retrieve import retrieve_node
from app.nodes.answer import answer_node
from app.nodes.personal import personal_node
from app.nodes.deflect import deflect_node
from app.nodes.offtopic import offtopic_node


class GraphState(TypedDict):
    question: str
    category: str
    context: str
    answer: str
    history: List[dict]


def route_after_classify(state: GraphState) -> str:
    return state["category"]


def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("classify", classify_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("answer", answer_node)
    graph.add_node("personal", personal_node)
    graph.add_node("deflect", deflect_node)
    graph.add_node("offtopic", offtopic_node)

    graph.set_entry_point("classify")
    graph.add_conditional_edges(
        "classify",
        route_after_classify,
        {
            "factual": "retrieve",
            "personal": "personal",
            "sensitive": "deflect",
            "offtopic": "offtopic",
        },
    )
    graph.add_edge("retrieve", "answer")
    graph.add_edge("answer", END)
    graph.add_edge("personal", END)
    graph.add_edge("deflect", END)
    graph.add_edge("offtopic", END)

    return graph.compile()


recruiterbot_graph = build_graph()


def ask(question: str) -> str:
    result = recruiterbot_graph.invoke(
        {"question": question, "category": "", "context": "", "answer": "", "history": []}
    )
    return result["answer"]