# 📄 PDF Knowledge Assistant  

A **Streamlit app** powered by [Phi Assistant](https://phi.ai/), `pgvector`, and `Postgres` that lets you **chat with your PDFs**.  
Upload any PDF, ask natural language questions, and get contextual answers based on the document.  

---

## ✨ Features
- 🔍 **Chat with PDFs** – Ask questions about the uploaded document.  
- 📂 **Upload your own PDFs** – Each PDF gets its own dedicated pgvector collection.  
- 🗄️ **Postgres + pgvector storage** – Efficient vector embeddings and persistent memory.  
- 💬 **Conversation history** – Keeps chat context per PDF.  
- 🌐 **Fallback demo** – If no PDF is uploaded, defaults to a sample *Thai Recipes* PDF.  

---

## 🛠️ Tech Stack
- [Streamlit](https://streamlit.io/) – Web UI  
- [Phi Assistant](https://phi.ai/) – Assistant framework  
- [Postgres + pgvector](https://github.com/pgvector/pgvector) – Vector database  
- [dotenv](https://pypi.org/project/python-dotenv/) – Environment management  

---

## ⚡ Setup Instructions

### 1. Clone this repo

git clone https://github.com/Viplove0114/pdf_assistant.git
cd pdf-assistant

### 2. Install dependencies
pip install -r requirements.txt


### 3. Start Postgres with pgvector

If you don’t have it already, run Postgres with pgvector:

docker run -d \
  --name pgvector \
  -e POSTGRES_USER=ai \
  -e POSTGRES_PASSWORD=ai \
  -e POSTGRES_DB=ai \
  -p 5532:5432 \
  ankane/pgvector

### 4. Configure environment variables

Create a .env file in the project root:
GROQ_API_KEY="your_groq_api_key_here"
PHI_API_KEY="your phidata api key here"

### 5. Run the Streamlit app
streamlit run streamlit_app.py

## 📂 Project Structure
.
|
├── pdf_assistant.py      # Original CLI version

├── streamlit_app.py      # Streamlit web app

├── requirements.txt      # Python dependencies

├── .env                  # Environment variables (not committed)

└── README.md             # This file


## 🚀 Usage

1. Start the app with streamlit run streamlit_app.py.

2. Upload a PDF file via the uploader.

3. Ask natural language questions in the chat box.

4. Get context-aware answers from your document.

If no PDF is uploaded, the app loads a Thai Recipes PDF demo.


## 🛡️ Notes

- Each uploaded PDF is indexed into its own pgvector collection (e.g., pdf_ab12cd34).

- Switching to a new PDF resets chat history.

- All assistant runs are stored in Postgres for persistence.



## 🙌 Acknowledgments

Phi
 for the Assistant framework.

pgvector
 for vector similarity search.

Streamlit
 for making UI simple and fun.
