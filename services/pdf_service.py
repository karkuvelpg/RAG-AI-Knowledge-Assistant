import os
from langchain_community.document_loaders import PyPDFLoader

def load_pdfs(uploaded_files):

    documents = []

    os.makedirs("static/uploads", exist_ok=True)

    for file in uploaded_files:

        file_path = os.path.join("static/uploads", file.name)

        with open(file_path, "wb") as f:
            f.write(file.read())

        loader = PyPDFLoader(file_path)

        docs = loader.load()

        for doc in docs:
            doc.metadata["source"] = file.name
            doc.metadata["page"] = doc.metadata.get("page", 0)

        documents.extend(docs)

    return documents