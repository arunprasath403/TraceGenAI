# TraceGenAI  
### Agentic AI for SDLC Traceability

**TraceGenAI** is an enterprise-grade **multi-agent AI system** that automates **SDLC traceability** by converting **requirements, design, and code context** into **validated, traceable test cases**, delivered as **Excel artifacts** for real-world QA and audit workflows.

The system is built with a **deterministic execution model**, **validation-first AI design**, and **security-aware architecture**, making it suitable for enterprise and compliance-driven environments.

---
```
flowchart TD
    A["Project / Business Context<br/>Requirements · Design · Codebase"]:::input
    A --> B["Requirements Agent<br/>Functional & Non-Functional Extraction<br/>Structured JSON Output"]:::agent
    B --> C["Design Agent<br/>Architecture Derivation<br/>Component Mapping"]:::agent
    C --> D["Code Analysis Agent<br/>API Extraction<br/>UI & Flow Identification"]:::agent
    D --> E["Test Case Generation Agent<br/>Enterprise Test Cases<br/>Full Traceability"]:::agent
    E --> F["Validation Layer<br/>Schema Enforcement<br/>Mandatory Field Checks"]:::validation
    F --> G["Excel Output<br/>QA-Ready XLSX<br/>Audit-Friendly Artifact"]:::output

    classDef input fill:#D6EBFF,stroke:#003366,stroke-width:2px,color:#000000;
    classDef agent fill:#E6DCFF,stroke:#2E0066,stroke-width:2px,color:#000000;
    classDef validation fill:#FFE0B2,stroke:#8A4B00,stroke-width:2px,color:#000000;
    classDef output fill:#C8F7C5,stroke:#1B5E20,stroke-width:2px,color:#000000;
```

## How the System Works

- The pipeline executes in a **fixed, deterministic order**
- Each agent has a **single, clearly defined responsibility**
- Outputs from one stage become **validated inputs** for the next
- LLMs are used only where reasoning is required
- A validation gate ensures **no untrusted AI output reaches final artifacts**

This mirrors how **real enterprise SDLC workflows** operate.

---

## Key Capabilities

- Multi-agent SDLC pipeline (requirements → design → code → tests)
- End-to-end traceability across all SDLC artifacts
- Validation-first AI (LLM output treated as untrusted)
- Code-aware test generation (no hallucinated APIs or flows)
- Excel-based output aligned with enterprise QA practices
- RAG-ready architecture for future grounding and reuse

---

## Getting Started (Clone & Run)

### Prerequisites
- Python 3.10 or higher  
- Git  
- An LLM provider account (OpenAI / OpenRouter compatible)

### 1. Clone the Repository
```bash
git clone https://github.com/arunprasath403/TraceGenAI.git
cd TraceGenAI
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\Scripts\activate
```

**Linux / macOS**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file **locally** (do not commit it):

```env
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL_NAME=gpt-4o-mini
LLM_TEMPERATURE=0.2
```

### 5. Run the Application (Streamlit UI)
```bash
python -m streamlit run ui/app.py
```

---

## Working on the Project

1. Update project context or input data  
2. Modify or extend individual agents  
3. Run the pipeline via Streamlit  
4. Validate generated test cases  
5. Review Excel output  

Each agent can be enhanced independently without impacting the rest of the pipeline.

---

## Project Structure

```text
agents/     multi-agent logic
tools/      validation, Excel generation, parsing
rag/        retrieval and vector store
utils/      shared project context
config/     settings and logging
ui/         Streamlit interface
main.py     pipeline orchestrator
```

---

## Security & Reliability

- No hardcoded secrets
- Environment-based configuration
- Strict output validation
- Prompt-injection-aware design
- Logging avoids sensitive data

---

## Use Cases

- Enterprise QA automation
- SDLC traceability and compliance
- AI-assisted manual testing
- Internal engineering tooling

---

## Author

**Arun Prasath**  
GenAI Engineer | Agentic AI | Enterprise Automation

---

### Final Note

TraceGenAI is built with a **production mindset**, not as a demo.  
The architecture emphasizes **clarity, control, and traceability**, which are essential for real-world SDLC automation.
