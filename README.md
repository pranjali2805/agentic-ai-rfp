# agentic-ai-rfp
Agentic AI system for automating B2B RFP response using multi-agent architecture.
#  Agentic AI – Automating B2B RFP Responses

###  Overview
An **AI-powered multi-agent system** that automates how enterprises respond to **B2B RFPs (Request for Proposals)**.  
The system uses separate **Sales**, **Technical**, and **Pricing** agents to parse documents, identify matching SKUs, calculate pricing, and auto-generate PowerPoint proposals.

Built with **Python + Streamlit**, this project demonstrates how **Agentic AI workflows** can streamline complex enterprise processes such as tender responses.

---

###  Features
-  **RFP Parsing** – Reads structured (PDF/JSON) and scanned RFPs using `pdfplumber` + `pytesseract` OCR  
-  **Multi-Agent Architecture** – Independent agents for Sales, Technical Matching, and Pricing  
-  **Explainable Matching** – Shows why each SKU was selected (e.g., based on keywords/specs)  
-  **Dynamic Pricing Engine** – Adjusts pricing based on quantity, urgency, and margin  
-  **Auto PPT Generation** – Creates ready-to-send PowerPoint proposal reports  
- **Streamlit Dashboard** – Modern, dark-themed interface for file upload, AI processing, and result download

---

###  Tech Stack
| Category | Tools |
|-----------|--------|
| Frontend | Streamlit |
| Backend | Python |
| AI/ML | LangChain (optional), Pandas, OCR (Tesseract) |
| Document Parsing | pdfplumber, pdf2image |
| Reporting | python-pptx |
| Deployment | Streamlit Cloud |

---

###  Project Structure
agentic-ai-rfp/
├── app.py # Main Streamlit app
├── sales_agent.py # Handles RFP parsing (JSON/PDF)
├── technical_agent.py # Matches RFP items with SKUs
├── pricing_agent.py # Calculates dynamic pricing
├── report_generator.py # Creates PowerPoint reports
├── data/
│ ├── Sample_RFP_Report.pdf
│ ├── mock_skus.csv
│ ├── sample_rfp.json
│ └── ...
└── requirements.txt


---

### Installation & Usage

#### Clone the Repository
```bash
git clone https://github.com/pranjali2805/agentic-ai-rfp.git
cd agentic-ai-rfp

