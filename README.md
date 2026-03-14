# 📚 RAG AI PDF Knowledge Assistant

This project builds an **AI-powered assistant that answers questions from PDF documents** using **Retrieval Augmented Generation (RAG)**.

Users can upload PDFs and ask questions. The system retrieves relevant content from the documents and generates answers using a **Large Language Model (LLM)**.

---

## 📌 Project Objective

* Build a **document question-answering system**
* Implement **Retrieval Augmented Generation (RAG)**
* Allow users to **query PDF documents interactively**
* Provide **source references (document + page number)** for answers

---

## 🛠️ Tech Stack

* Python 3
* Streamlit
* LangChain
* FAISS / Vector Store
* Sarvam Platform / LLM API
* PyPDFLoader

---

## 📂 Project Structure

```
RAG-AI-Knowledge-Assistant/
│
├── app.py
├── rag_engine.py
├── config.py
├── requirements.txt
├── README.md
│
├── services/
│   └── pdf_service.py
│   └── pdf_service.py
│
└── static/
    └── uploads/
```

---

## 🔍 System Workflow

The application follows the **RAG pipeline**:

1️⃣ Upload PDF documents
2️⃣ Extract text from PDFs
3️⃣ Split text into chunks
4️⃣ Convert chunks into vector embeddings
5️⃣ Store embeddings in a vector database
6️⃣ Retrieve relevant chunks for user queries
7️⃣ Generate answers using an LLM

---

## 🤖 Features

* Upload **multiple PDF documents**
* Ask questions about uploaded documents
* AI-generated answers using **RAG**
* Display **source file and page number**
* **Streaming response** (typing effect)
* **Copy AI responses**
* **Edit / Delete previous questions**
* Handles **small talk messages** (like "thanks", "ok")

---

## 📊 Example Interaction

User Question:

```
What is a Large Language Model?
```

AI Response:

```
Large Language Models (LLMs) are AI systems trained on vast amounts of text data to understand and generate human-like language.

Sources:
Generative-AI-and-LLMs-for-Dummies.pdf — Page 7
```

---

## ▶️ How to Run the Project

### 1️⃣ Clone the repository

```
git clone https://github.com/karkuvelpg/RAG-AI-Knowledge-Assistant.git
cd RAG-AI-Knowledge-Assistant
```

---

### 2️⃣ Create virtual environment

```
conda create -n rag_env python=3.10
conda activate rag_env
```

or

```
python -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

---

### 4️⃣ Add API key

Create a `.env` file:

```
SARVAM_API_KEY=your_api_key_here
```

---

### 5️⃣ Run the application

```
streamlit run app.py
```

---

## 🎓 Learning Outcomes

* Understanding **Retrieval Augmented Generation**
* Working with **LangChain pipelines**
* Implementing **vector search**
* Building **LLM-powered applications**
* Creating interactive **Streamlit AI interfaces**

---

## 🔮 Future Improvements

* Highlight source text inside PDFs
* PDF page preview popup
* Conversation memory
* Improved semantic search
* Cloud deployment

---

## 👨‍💻 Author

**Karkuvel P**

M.Sc Mathematics
Aspiring Machine Learning Engineer

GitHub
https://github.com/karkuvelpg

---

⭐ If you find this project useful, please give it a star!
