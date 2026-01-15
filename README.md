# 🛡️ LogOps AI: Real-Time DevOps Error Resolver

LogOps AI is an intelligent Site Reliability Engineering (SRE) tool designed to automate the detection, analysis, and resolution of live cloud infrastructure errors.

Unlike standard log viewers, LogOps AI uses a Retrieval-Augmented Generation (RAG) pipeline to consult an internal Knowledge Base (SOPs) before prescribing a fix. It acts as a Level-1 AI Engineer that watches a live log stream, detects critical failures in real-time, and generates precise CLI commands or SQL queries to fix them—strictly adhering to company policies.

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.10+
- Ollama installed and running  
  https://ollama.com

Pull the Llama 3 model:
ollama run llama3

---

### Step 1: Clone the Repository
git clone https://github.com/YashShedge503/glidecloud.git

cd glidecloud/Genai_capstone_project

---

### Step 2: Create Virtual Environment
python -m venv venv

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

---

### Step 3: Install Dependencies
pip install -r requirements.txt

---

## 📸 Usage (How to Run the Demo)

To demonstrate real-time behavior, use two terminal windows.

---

### Terminal 1: Start the Simulation Server
Acts as the production environment generating live logs.

python log_emitter.py

Logs will be written every few seconds, including simulated failures.

---

### Terminal 2: Start the LogOps Dashboard
Acts as the SRE monitoring system.

streamlit run main.py

---

## 🎬 Workflow Demo

1. Watch Terminal 1 until a red ERROR or CRITICAL log appears  
   (e.g., TokenExpiredError)

2. Open the dashboard and click "Poll Log Stream"

3. The error instantly appears in the Pending list

4. Select the error and click "Auto-Resolve"

5. The AI:
   - Explains the root cause
   - Retrieves the correct SOP
   - Generates the exact fix command

---

## 🏗️ System Architecture

The system follows a Real-Time Producer-Consumer architecture designed to mimic professional DevOps monitoring environments (like Splunk or Datadog).

### 1️⃣ The Producer (Log Simulation)
Script: log_emitter.py

- Acts as a production server cluster
- Generates a continuous stream of logs (INFO, ERROR, CRITICAL)
- Writes logs to a shared file (real_time_logs.txt) every few seconds

Tech: Python, Logging Module

---

### 2️⃣ The Consumer (Ingestion Layer)
Script: src/ingestion.py

- Tails the log file in real-time
- Filters out noisy INFO logs
- Captures only ERROR and CRITICAL events
- Normalizes logs into structured database records

Tech: Python File I/O, Regex

---

### 3️⃣ The Brain (RAG Engine)
Script: src/rag.py

- Converts internal troubleshooting SOPs into vector embeddings
- Enables semantic policy search

Tech: ChromaDB, HuggingFace Embeddings

---

### 4️⃣ The Resolver (AI Agent)
Script: src/llm.py

- Retrieves the exact SOP for the detected error
- Prompts the LLM with:
  - Error log
  - Internal policy
  - Operational constraints
- Generates a compliant, executable fix

Tech: LangChain, Ollama (Llama 3)

---

### 5️⃣ The Dashboard (Frontend)
Script: main.py

- Interactive monitoring dashboard for SREs
- Displays live alerts and supports auto-resolution

Tech: Streamlit

---

## 🧠 The RAG Pipeline (True RAG)

This project implements True RAG to ensure the AI follows internal company rules instead of hallucinating generic fixes.

### Knowledge Base
- knowledge_base/troubleshooting_manual.txt
- Contains confidential SOPs  
- Example: Do not restart the payment service during business hours

### Vectorization
- SOPs are chunked and embedded using all-MiniLM-L6-v2

### Context Retrieval
- When an error occurs (e.g., Payment Timeout)
- ChromaDB retrieves the exact policy for that service

### Augmented Prompting
- LLM receives:
  - Error Log
  - Internal Policy
  - Operational Constraints

Result: A compliance-safe, production-ready fix

---

## 🚀 Features

⚡ Real-Time Log Streaming  
🔍 Intelligent Filtering (ERROR / CRITICAL only)  
🤖 Auto-Resolution with real CLI commands (kubectl, systemctl, npm, SQL)  
🔒 Policy Enforcement using RAG  
📊 Live Interactive Dashboard  

---

## 🛠️ Tech Stack

- Language: Python 3.10+
- Frontend: Streamlit
- AI / LLM: Ollama (Llama 3)
- Orchestration: LangChain
- Vector Database: ChromaDB
- Database: SQLite (SQLAlchemy)
- Embeddings: HuggingFace (sentence-transformers)

---

## ✅ Outcome

LogOps AI demonstrates a production-ready approach to AI Ops by answering one critical question:

How can we trust AI to fix our servers?

Answer: By grounding every decision in verified internal policies using Retrieval-Augmented Generation.
