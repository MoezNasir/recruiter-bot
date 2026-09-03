from typing import Literal
from pydantic import BaseModel, Field
from app.utils.llm import get_llm

CLASSIFY_PROMPT = """You are routing a recruiter's question about a job candidate into exactly one category.

Categories:
- factual: skills, work experience, education, certifications, specific project names,
  technical stack, tools/technologies used, dates of employment, responsibilities
- personal: career goals, work style, motivations, hobbies, greetings (hi/hello),
  introductions/small talk, culture fit, availability/notice period, why they're
  job searching
- sensitive: salary/compensation expectations, immigration/visa status, age, marital
  status, religion, disability, relationships, or any private/legally protected data
- offtopic: unrelated to the candidate entirely (math problems, recipes, general coding
  help, questions about the recruiter's own company, or anything not about this person)

Rules:
- Choose the category that best matches the PRIMARY intent of the question. If a
  question mixes categories (e.g. "what's your visa status and can you start Monday"),
  classify by the more sensitive/restrictive category present.
- Short greetings or vague openers ("hi", "tell me about yourself") are personal, not offtopic.
- If genuinely ambiguous between factual and personal, prefer factual — it's safer to
  answer with concrete resume details than to speculate about traits.
- Ignore phrasing/politeness; classify based on subject matter only.

Respond with ONLY the category name, lowercase, no punctuation or explanation:
factual, personal, sensitive, or offtopic

Question: {question}"""

class Classification(BaseModel):
    category: Literal["factual", "personal", "sensitive", "offtopic"] = Field(
        description="The routing category for this question"
    )


def classify_node(state: dict) -> dict:
    llm = get_llm(temperature=0)
    # method="json_schema" uses Groq's native structured-output mechanism.
    # The default ("function_calling") relies on forced tool-calling, which
    # openai/gpt-oss-120b doesn't reliably honor — it can return plain text
    # instead of calling the tool, which is what caused the 400 error.
    structured_llm = llm.with_structured_output(Classification, method="json_schema")
    result = structured_llm.invoke(CLASSIFY_PROMPT.format(question=state["question"]))
    state["category"] = result.category
    return state