# ai/chatbot.py
import os
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from typing import TypedDict

from ai.rag import load_retriever

class ChatState(TypedDict):
    question: str
    context: str
    answer: str

# setup retriever + LLM
retriever = load_retriever()
llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=os.getenv("OPENAI_API_KEY"))

def retrieve(state: ChatState):
    docs = retriever.invoke("query")
    state["context"] = "\n".join([d.page_content for d in docs])
    return state

def generate(state: ChatState):
    prompt = f"""You are a SOC analyst assistant. 
Question: {state['question']}
Context: {state['context']}
Answer clearly:"""
    resp = llm.invoke(prompt)
    state["answer"] = resp.content
    return state

# build workflow
workflow = StateGraph(ChatState)
workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

chatbot = workflow.compile()
