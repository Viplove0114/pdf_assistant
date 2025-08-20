import streamlit as st
from phi.assistant import Assistant
from phi.storage.assistant.postgres import PgAssistantStorage
from phi.knowledge.pdf import PDFUrlKnowledgeBase, PDFFileKnowledgeBase
from phi.vectordb.pgvector import PgVector2
import os
from dotenv import load_dotenv
import tempfile
import uuid

# Load environment variables
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Database connection
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# Storage
storage = PgAssistantStorage(table_name="pdf_assistant", db_url=db_url)

# Streamlit page setup
st.set_page_config(page_title="PDF Assistant", page_icon="📄")
st.title("📄 PDF Knowledge Assistant")

# File uploader
uploaded_file = st.file_uploader("📂 Upload a PDF to query", type=["pdf"])

# Knowledge base setup
if uploaded_file:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        pdf_path = tmp_file.name

    # Create a unique collection name for this PDF
    collection_name = f"pdf_{uuid.uuid4().hex[:8]}"

    # Build knowledge base from uploaded PDF
    knowledge_base = PDFFileKnowledgeBase(
        files=[pdf_path],
        vector_db=PgVector2(collection=collection_name, db_url=db_url)
    )
    knowledge_base.load()
    st.success(f"✅ PDF uploaded and indexed with collection: {collection_name}")

else:
    # Default knowledge base (Thai recipes demo)
    collection_name = "recipes"
    knowledge_base = PDFUrlKnowledgeBase(
        urls=["https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
        vector_db=PgVector2(collection=collection_name, db_url=db_url)
    )
    knowledge_base.load()
    st.info("ℹ️ No PDF uploaded — using Thai Recipes demo")

# Initialize assistant once
if "assistant" not in st.session_state or st.session_state.get("collection") != collection_name:
    run_id = None
    existing_run_ids = storage.get_all_run_ids("user")
    if existing_run_ids:
        run_id = existing_run_ids[0]

    st.session_state.assistant = Assistant(
        run_id=run_id,
        user_id="user",
        knowledge_base=knowledge_base,
        storage=storage,
        show_tool_calls=True,
        search_knowledge=True,
        read_chat_history=True,
    )
    st.session_state.collection = collection_name
    st.session_state.messages = []  # reset chat history per PDF

# Display chat history
for role, msg in st.session_state.messages:
    if role == "user":
        st.chat_message("user").markdown(msg)
    else:
        st.chat_message("assistant").markdown(msg)

# Chat input
if prompt := st.chat_input("Ask me something about the PDF..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append(("user", prompt))

    response = st.session_state.assistant.run(prompt)
    st.chat_message("assistant").markdown(response)
    st.session_state.messages.append(("assistant", response))
