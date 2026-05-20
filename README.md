# SimplifIQ Lead Enricher & Strategic Audit Engine

An asynchronous, production-grade backend pipeline built with FastAPI. This system accepts incoming sales leads, instantly web-scrapes target business domains, processes raw text using Llama-3.1 via Groq cloud inference, builds polished PDF business briefs, and dispatches them straight to the user via secure SMTP email layers.

## ⚙️ Architecture & Data Flow

1. **FastAPI Ingestion Endpoint:** Captures incoming lead payloads (`/api/leads`).
2. **Asynchronous Background Worker:** Immediately releases the HTTP connection back to the client while spawning a background thread execution loop.
3. **Web Scraper (BeautifulSoup4):** Parses target endpoints to extract raw semantic text context.
4. **AI Inference Engine (Groq / Llama-3.1-8b):** Transforms raw text payloads into highly curated business growth strategies.
5. **PDF Generator (FPDF2):** Dynamically builds professional visual reports with native error containment guards.
6. **SMTP Email Relayer:** Packages assets into multi-part MIMEs and safely delivers them via Google App security protocols.

---

## 🛠️ Tech Stack & Dependencies

* **Framework:** FastAPI (Asynchronous Python Web Framework)
* **Web Scraping:** BeautifulSoup4 & HTTPX
* **AI Engine:** Groq SDK (`llama-3.1-8b-instant`)
* **Document Generation:** FPDF2
* **Environment Management:** Pydantic-Settings (Safe `.env` initialization)

---

## 🚀 Local Installation & Set Up

### 1. Clone & Set Up Virtual Environment
```bash
git clone https://github.com/Abdul-Mannan-Codes/simplifiq-lead-enricher.git
cd simplifiq-lead-enricher
python -m venv venv
source venv/Scripts/activate  # On Windows Windows
```
### 2. Install dependencies
```bash
pip install fastapi uvicorn beautifulsoup4 httpx groq fpdf2 pydantic-settings
```

### 3. Configure local variables
Create a hidden .env file in the root folder
```bash
GROQ_API_KEY=your_groq_api_key_here
SENDER_EMAIL=your_auth_gmail@gmail.com
SENDER_PASSWORD=your_16_digit_google_app_password
```

### 4. Fire up the server
```bash
uvicorn main:app --reload
```

### 5. Navigate to the live server to interact with the system
```bash
http://127.0.0.1:8000/docs
```

