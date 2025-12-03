#**Steve Jobs AI Advisor — RAG-Powered AI Assistant**

A retrieval-augmented AI system that blends **Steve Jobs’ communication style, philosophy, and structured thinking** with modern AI retrieval and generation.

This project enables users to:

* Ask questions about design, innovation, leadership, failure, creativity, and life
* Receive answers in **Steve Jobs’ characteristic tone** — bold, layered, intuitive, and philosophical
* Ground the responses in **real documents** via FAISS-powered retrieval
* Optionally listen to the answers through high-quality OpenAI TTS

It is built using:

* **OpenAI GPT models**
* **FAISS vector search**
* **LangChain 0.2+ modular components**
* **Gradio interface**
* **Cleanly separated folder architecture (core/services/interface/config)**

This creates an experience that feels like you’re *“asking Jobs for advice… and he actually answers.”*

---

#**Features**

###**Steve Jobs Persona Engine**

A handcrafted persona prompt + formatting system that ensures responses feel authentic.
The system:

* Uses layered reasoning structure
* Starts with a bold, simple statement
* Adds 2–3 deep insights
* Closes with intuitive, actionable wisdom
* Optionally rewrites using Jobs-style pacing, clarity, and simplicity

###**RAG (Retrieval-Augmented Generation)**

* Upload PDFs / DOCX / TXT
* Extract text automatically
* Chunk with LangChain text splitters
* Store embeddings in FAISS
* Retrieve highly relevant passages
* Feed into the LLM for grounded, accurate answers

###**Text-to-Speech**

* Uses OpenAI TTS (`onyx` voice)
* Converts persona responses to speech
* Saves as high-quality `.mp3`

###**Gradio Interface**

* Ask questions
* Optional context
* Toggle voice output
* View or listen to answers
* Rebuild FAISS index
* Check system status
* Provide feedback (Excel logging)

---

#**Project Structure**

```
rag/
¦
+-- run.py
+-- requirements.txt
+-- README.md
+-- .gitignore
¦
+-- data/
¦   +-- vector.index
¦   +-- *.pdf / *.txt / *.docx
¦
+-- src/
    +-- config/
    ¦   +-- settings.py
    ¦
    +-- core/
    ¦   +-- vector_store.py
    ¦   +-- llm_handler.py
    ¦   +-- rag_pipeline.py
    ¦   +-- text_splitter.py
    ¦
    +-- services/
    ¦   +-- document_processor.py
    ¦   +-- tts_service.py
    ¦   +-- feedback_service.py
    ¦
    +-- interface/
        +-- gradio_app.py
        +-- handlers.py
```

---

#Installation

```bash
git clone https://github.com/yourusername/rag-project.git
cd rag-project
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

#Environment Variable

```bash
setx OPENAI_API_KEY "your_api_key_here"
```

---

#Run the App

```bash
python run.py
```

Gradio will open at:

```
http://localhost:7860
```

---

#Add Your Documents

Place files into:

```
data/
```

Then click **Rebuild Index** from the UI.

---

#Configuration

All app settings are in:

```
src/config/settings.py
```

You can modify:

* Model name
* TTS voice
* Chunk size
* FAISS paths
* Debug mode

---

#Requirements

```
gradio
openai
faiss-cpu
python-docx
PyPDF2
langchain-core
langchain-community
langchain-openai
langchain-text-splitters
openpyxl
tqdm
```

---

#Contributions

Pull requests and feature suggestions are welcome.

---

#License

MIT License.

