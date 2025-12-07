# HYBRID RAG SYSTEM — FINAL VERSION

import os
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

DB_PATH = "faiss_store"


# ---------------------------------------------------------
# Load FAISS vector store
# ---------------------------------------------------------
def load_vector_store():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vector_db = FAISS.load_local(
        DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vector_db


# ---------------------------------------------------------
# Build RAG chain
# ---------------------------------------------------------
def build_rag_chain(vector_db):

    retriever = vector_db.as_retriever(search_kwargs={"k": 8})

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    rag_prompt = PromptTemplate(
        input_variables=["history", "context", "question"],
        template="""
You are a helpful support assistant for ProjectPartner.

Conversation so far:
{history}

Answer using ONLY the provided context. 
If context does NOT contain the answer, respond EXACTLY with:
"I_DONT_KNOW_FROM_RAG"

Context:
{context}

Question:
{question}

Answer:
"""
    )

    extract_question = RunnableLambda(lambda x: x["question"])

    rag_chain = (
        RunnableParallel({
            "context": extract_question | retriever,
            "question": RunnablePassthrough(),
            "history": RunnablePassthrough()
        })
        | rag_prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


# ---------------------------------------------------------
# Fallback LLM (Smart reasoning)
# ---------------------------------------------------------
def build_fallback_chain():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.2
    )

    fallback_prompt = PromptTemplate(
        input_variables=["history", "question"],
        template="""
You are an intelligent support assistant for ProjectPartner.

Conversation so far:
{history}

TYou are ProjectPartner's intelligent support assistant.

Conversation so far:
{history}

The retrieval system did not find any specific guidance for this question.

Your job is to give the **best helpful explanation** based on platform rules:
- Projects cannot be deleted.
- Only authors can close their project.
- A closed project stays visible but stops new join requests.
- Guests cannot post projects, message, or send join requests.
- Authors can accept or decline join requests.
- If user says thank you, fine, okay,ohk, done, got it,  or similar kind of guestures, respond Sure! Let me know if you need help with anything else 😊.

ABSOLUTE RULES:
- NEVER mention documentation or context.
- NEVER mention RAG, retrieval, system, or missing information.
- NEVER say “not listed in docs”.
- NEVER guess UI steps that are not explicitly known.
- NEVER hallucinate new platform features.
- ONLY explain what users CAN do based on rules.
- If exact steps are unknown, say:
  "Here is how this works on ProjectPartner" — and explain the feature, not the steps.

User Question:
{question}

Helpful Answer:
"""
    )

    return fallback_prompt | llm | StrOutputParser()


# ---------------------------------------------------------
# LOAD EVERYTHING ONCE (Important for Render)
# ---------------------------------------------------------

VECTOR_DB = load_vector_store()
RAG_CHAIN = build_rag_chain(VECTOR_DB)
FALLBACK_CHAIN = build_fallback_chain()


# ---------------------------------------------------------
# PUBLIC FUNCTION FOR API
# ---------------------------------------------------------
def rag_query(question: str, history: str = "") -> str:
    """
    API-callable function:
    - handles small talk
    - runs hybrid RAG
    - falls back if needed
    - returns answer as string
    """

    SMALL_TALK = [
        "ok", "okay", "oky", "k", "kk",
        "thanks", "thank you", "thx",
        "got it", "cool", "nice", "great", "good", "alright"
    ]

    # --- SMALL TALK HANDLER (no RAG, no fallback) ---
    if question.lower().strip() in SMALL_TALK:
        return "Sure! Let me know if you need help with anything else 😊"

    final_input = {
        "history": history,
        "question": question
    }

    try:
        rag_answer = RAG_CHAIN.invoke(final_input)

        # Trigger fallback if needed
        if "I_DONT_KNOW_FROM_RAG" in rag_answer:
            return FALLBACK_CHAIN.invoke(final_input)

        return rag_answer

    except Exception as e:
        print("RAG ERROR →", e)
        return "Something went wrong while processing your question."


# OPTIONAL: Local console test
if __name__ == "__main__":
    while True:
        q = input("You: ")
        print("Bot:", rag_query(q))
