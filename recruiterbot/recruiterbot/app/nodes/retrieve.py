from app.utils.retriever import retrieve_chunks


def retrieve_node(state: dict) -> dict:
    state["context"] = retrieve_chunks(state["question"], k=4)
    return state