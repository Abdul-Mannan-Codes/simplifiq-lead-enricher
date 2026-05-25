# SimplifIQ Lead Enricher & Strategic Audit Engine

An asynchronous, production-grade backend pipeline built with FastAPI. This system accepts incoming sales leads, orchestrates stealth data extraction via the Haunt API, processes structured JSON payloads using Llama-3.1 via Groq cloud inference, builds polished PDF business briefs, and dispatches them straight to the user via secure SMTP email layers.

## 🔌 Automated Data Pipeline Architecture

The system processes lead URLs through a robust, dual-layer extraction and parsing pipeline before generating the final strategic brief:

1. **Primary Extraction (Haunt API):** Safely handles protocol injections, bypasses bot detection, and extracts highly structured, clean JSON parameters (`core_services`, `market_positioning`, `icp`).
2. **AI Reasoning Engine (Groq + Llama 3.1):** Consumes the clean JSON payload, applying targeted B2B consulting frameworks to generate actionable insights while enforcing strict HTML compilation tags for pdf compatibility.
3. **Document Compilation (FPDF2):** Programmatically processes the AI text, applying regex safeguards to clean markdown artifacts and render native inline typography layouts via `write_html()`.

### 🛡️ Reliability & Failover Mechanisms

* **Data-Absence Fallback:** If a scraped website returns no context or is completely blank, the Groq engine automatically catches the condition and pivots to generating high-value domain-standard optimizations based on the company's industry sector.
* **Scraper Failover Layer:** In the event of Haunt API token depletion or service downtime, the pipeline is architected to gracefully degrade. The legacy manual scraping module (`BeautifulSoup4`) is retained at the base of the pipeline as an emergency fallback to preserve system uptime.

## ⚙️ Architecture & Data Flow

1. **FastAPI Ingestion Endpoint:** Captures incoming lead payloads (`/api/leads`).
2. **Asynchronous Background Worker:** Immediately releases the HTTP connection back to the client while spawning a background thread execution loop.
3. **Primary Web Scraper (Haunt API):** Parses target endpoints to extract raw semantic text context or structured business payloads.
4. **AI Inference Engine (Groq / Llama-3.1-8b):** Transforms raw text payloads into highly curated business growth strategies in a direct, client-facing ("your") tone.
5. **PDF Generator (FPDF2):** Dynamically processes custom-formatted HTML typography strings and builds professional visual reports with native error containment guards.
6. **SMTP Email Relayer:** Packages assets into multi-part MIMEs and safely delivers them via Google App security protocols.

---

## 🛠️ Tech Stack & Dependencies

* **Framework:** FastAPI (Asynchronous Python Web Framework)
* **Web Scraping:** Haunt API (Primary) & BeautifulSoup4 / HTTPX (Fallback Layer)
* **AI Engine:** Groq SDK (`llama-3.1-8b-instant`)
* **Document Generation:** FPDF2 (`write_html` architecture)
* **Environment Management:** Pydantic-Settings (Safe `.env` initialization)

---

## 🚀 Local Installation & Set Up

### 1. Clone & Set Up Virtual Environment
```bash
git clone https://github.com/Abdul-Mannan-Codes/simplifiq-lead-enricher.git
cd simplifiq-lead-enricher
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install fastapi uvicorn beautifulsoup4 httpx groq fpdf2 pydantic-settings
```

### 3. Configure local variables
Create a hidden .env file in the root folder.
```bash
GROQ_API_KEY=your_groq_api_key_here
HAUNT_API_KEY=your_haunt_api_key_here
SENDER_EMAIL=your_auth_gmail@gmail.com
SENDER_PASSWORD=your_16_digit_google_app_password
```

### 4. Fire up the server
```bash
uvicorn main:app --reload
```

### 5. Navigate to the live server to interact with the system
```bash
http://127.0.0.1:8000/
```