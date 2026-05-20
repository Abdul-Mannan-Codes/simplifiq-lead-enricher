import os
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

# --- NEW: Automatically load the hidden .env file into Python's memory ---
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GROQ_API_KEY: str
    SENDER_EMAIL: str = ""
    SENDER_PASSWORD: str = ""

    class Config:
        env_file = ".env"

# Instantly load and inject the keys into your system environment variables
try:
    settings = Settings()
    os.environ["GROQ_API_KEY"] = settings.GROQ_API_KEY
    os.environ["SENDER_EMAIL"] = settings.SENDER_EMAIL
    os.environ["SENDER_PASSWORD"] = settings.SENDER_PASSWORD
    print("🚀 [Environment] .env variables loaded successfully into system memory!")
except Exception as e:
    print(f"⚠️ [Environment] Warning loading .env file: {e}")
# ------------------------------------------------------------------------

# Import the specialized helper functions we wrote in our services folder
from services.scraper import scrape_website
from services.ai_engine import generate_insights
from services.pdf_generator import create_pdf
from services.email_service import send_report_email

# (The rest of your main.py code below remains exactly the same...)
# 1. Initialize the FastAPI Application
app = FastAPI(
    title="SimplifIQ Lead Automation Engine",
    description="Asynchronously enriches lead info, runs Llama-3 AI analytics, generates custom PDFs, and triggers automated emailing."
)

# 2. Allow our frontend form to talk to our backend (CORS configuration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows any local frontend or browser form to hit this API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Define the Incoming Form Data Structure (Data Validation)
class LeadFormInput(BaseModel):
    fullName: str
    email: EmailStr  # Pydantic automatically checks if this is a real email syntax
    companyName: str
    website: str     # Expects a valid website string URL

# 4. The Core Automation Pipeline Execution Loop
def automated_onboarding_pipeline(lead: LeadFormInput):
    """
    This function runs entirely in a background thread.
    It executes the heavy, slow steps one-by-one without blocking the web user.
    """
    print(f"\n⚡ [Pipeline Launched] Processing lead for: {lead.fullName} ({lead.companyName})")
    
    # Step A: Scrape the target website (Defensive programming: returns "" if fails)
    scraped_context = scrape_website(lead.website)
    print(f"   └─ Step 1 Complete: Web Scraping extracted {len(scraped_context)} characters.")
    
    # Step B: Call Groq Cloud Llama-3 API for hyper-targeted insights
    ai_insights = generate_insights(lead.companyName, scraped_context)
    print("   └─ Step 2 Complete: Llama-3 Insights formulated successfully.")
    
    # Step C: Generate the styled PDF report document
    generated_pdf_filename = create_pdf(lead.companyName, lead.fullName, ai_insights)
    print(f"   └─ Step 3 Complete: Layout compiled. File saved as {generated_pdf_filename}")
    
    # Step D: Shoot out the automated email containing the PDF attachment
    send_report_email(lead.email, lead.fullName, generated_pdf_filename)
    print(f"🏁 [Pipeline Complete] Finished processing workflow for {lead.companyName}!\n")

# 5. The Public-Facing API Endpoint
@app.post("/api/leads")
async def register_new_lead(lead_data: LeadFormInput, background_tasks: BackgroundTasks):
    """
    This route receives data from the user form. It hands over the slow processing tasks
    to FastAPI's BackgroundTasks worker queue and instantly returns a success message.
    """
    # Throw the processing chain into a background thread
    background_tasks.add_task(automated_onboarding_pipeline, lead_data)
    
    # Instantly tell the frontend form user that we received their data!
    # This prevents the website from freezing or hanging for 20 seconds.
    return {
        "status": "success",
        "message": f"Welcome {lead_data.fullName}! Your customized strategic audit report is being generated and will be sent to {lead_data.email} in a moment."
    }