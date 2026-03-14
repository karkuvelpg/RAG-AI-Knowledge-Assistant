from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import re

from services.llm_service import call_llm
from config import TOP_K

embeddings = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
)

def create_vector_store(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 50
    )

    chunks = splitter.split_documents(documents)

    vectorstore = FAISS.from_documents(chunks, embeddings)

    return vectorstore

def ask_question(vectorstore, question):
    retriever = vectorstore.as_retriever(search_kwargs ={"k": TOP_K})

    docs = retriever.invoke(question)

    context = ""
    sources = []

    for doc in docs:
        context += doc.page_content + "\n\n"

        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", 0) + 1

        if (source, page) not in sources:
            sources.append((source, page))

    prompt = f"""
You are an AI assistant called AI PDF Knowledge Assistant.

Rules:

1. If user asks "who are you":
   say "I am an AI PDF Knowledge Assistant that answers questions from uploaded PDFs."

2. If user asks "who created you":
   say "This AI PDF Knowledge Assistant was created by Karkuvel P."

3. Answer using ONLY the context below with bullet style point by point.

4. If answer not found say:
   "I cannot find the answer in the uploaded documents."

Context:
{context}

Question:
{question}
"""

    answer = call_llm(prompt)
    answer = re.sub(r"<think>", "", answer, flags=re.DOTALL)
    answer = answer.strip()

    system_answers = [
        "AI PDF Knowledge Assistant",
        "created by Karkuvel"
    ]

    if any(x.lower() in answer.lower() for x in system_answers):
        sources = []

    if "cannot find the answer" in answer.lower():
        sources = []

    return answer, sources
