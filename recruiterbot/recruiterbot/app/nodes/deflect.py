from app.utils.context import get_deflection_message


def deflect_node(state: dict) -> dict:
    state["answer"] = get_deflection_message()
    return state