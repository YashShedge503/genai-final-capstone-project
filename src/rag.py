import os
import shutil
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "chroma_db")
MANUAL_PATH = os.path.join(BASE_DIR, "knowledge_base", "troubleshooting_manual.txt")

class RagEngine:
    def __init__(self):
        print("⚙️ Initializing RAG Engine...")
        # Setup Embeddings (Small, fast model)
        self.embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Check if DB exists. If not, build it.
        if not os.path.exists(DB_PATH):
            print(f"⚡ Vector DB not found at {DB_PATH}. Building from manual...")
            self.build_vector_db()
        else:
            print("✅ Vector DB loaded from disk.")
            
        # Load DB connection
        self.vector_db = Chroma(persist_directory=DB_PATH, embedding_function=self.embedding_function)

    def build_vector_db(self):
        if not os.path.exists(MANUAL_PATH):
            print(f"❌ ERROR: Manual not found at {MANUAL_PATH}")
            return

        # Load Text
        loader = TextLoader(MANUAL_PATH)
        documents = loader.load()
        
        # Split into chunks (Paragraphs)
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_documents(documents)
        
        # Create DB
        Chroma.from_documents(
            documents=chunks, 
            embedding=self.embedding_function, 
            persist_directory=DB_PATH
        )
        print(f"🎉 Created Vector DB with {len(chunks)} knowledge chunks.")

    def retrieve(self, query, k=1):
        """Finds the 1 most relevant SOP section"""
        try:
            results = self.vector_db.similarity_search(query, k=k)
            if results:
                return results[0].page_content
            return "No specific SOP found in Knowledge Base."
        except Exception as e:
            return f"RAG Retrieval Error: {str(e)}"

# Singleton Instance (This is what llm.py imports)
rag = RagEngine()



# import os
# import shutil
# from langchain_community.document_loaders import TextLoader
# from langchain_text_splitters import CharacterTextSplitter
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_chroma import Chroma

# # Paths
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# DB_PATH = os.path.join(BASE_DIR, "chroma_db")
# MANUAL_PATH = os.path.join(BASE_DIR, "knowledge_base", "troubleshooting_manual.txt")

# class RagEngine:
#     def __init__(self):
#         print("⚙️ Initializing RAG Engine...")
#         # Setup Embeddings (Small, fast model)
#         self.embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
#         # Check if DB exists. If not, build it.
#         if not os.path.exists(DB_PATH):
#             print(f"⚡ Vector DB not found at {DB_PATH}. Building from manual...")
#             self.build_vector_db()
#         else:
#             print("✅ Vector DB loaded from disk.")
            
#         # Load DB connection
#         self.vector_db = Chroma(persist_directory=DB_PATH, embedding_function=self.embedding_function)

#     def build_vector_db(self):
#         if not os.path.exists(MANUAL_PATH):
#             print(f"❌ ERROR: Manual not found at {MANUAL_PATH}")
#             return

#         # Load Text
#         loader = TextLoader(MANUAL_PATH)
#         documents = loader.load()
        
#         # Split into chunks (Paragraphs)
#         text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
#         chunks = text_splitter.split_documents(documents)
        
#         # Create DB
#         Chroma.from_documents(
#             documents=chunks, 
#             embedding=self.embedding_function, 
#             persist_directory=DB_PATH
#         )
#         print(f"🎉 Created Vector DB with {len(chunks)} knowledge chunks.")

#     def retrieve(self, query, k=1):
#         """Finds the 1 most relevant SOP section"""
#         try:
#             results = self.vector_db.similarity_search(query, k=k)
#             if results:
#                 return results[0].page_content
#             return "No specific SOP found in Knowledge Base."
#         except Exception as e:
#             return f"RAG Retrieval Error: {str(e)}"

# # Singleton Instance
# rag = RagEngine()