OFFTOPIC_MESSAGE = (
    "That's outside what I'm here to help with — I'm set up to answer "
"questions about my background, skills, and experience (or just say hi!). "
"Feel free to ask me something along those lines."
)


def offtopic_node(state: dict) -> dict:
    state["answer"] = OFFTOPIC_MESSAGE
    return state