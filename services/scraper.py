import requests
from bs4 import BeautifulSoup
import httpx
import logging
import os

    
#Scraping using Haunt API - default

logger = logging.getLogger(__name__)

async def extract_company_insights(company_url: str) -> dict:
    """
    Extracts structured company insights using Haunt API.
    Falls back to a dictionary if the request fails.
    """
    # 1. Fetch the secret key from your environment setup
    haunt_key = os.getenv("HAUNT_API_KEY")
    if not haunt_key:
        logger.error("HAUNT_API_KEY is missing from environment variables.")
        raise ValueError("Configuration error: Missing API Key")

    # 2. Set up the exact endpoints and headers requested by Haunt
    endpoint = "https://hauntapi.com/v1/extract"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": haunt_key  # Direct match to their first-call guide!
    }

    # 3. Create your custom prompt to guide the AI extraction
    # You can ask for everything in a single prompt to get a clean response!
    prompt_instruction = (
        "Analyze this company website and extract the following structured details: "
        "1. Core Services/Products offered "
        "2. Market Positioning or Unique Value Proposition (UVP) "
        "3. Ideal Customer Profile (ICP) "
        "4. Key sales triggers or contact cues."
    )

    payload = {
        "url": company_url,
        "prompt": prompt_instruction
    }

    # 4. Execute the async network call
    async with httpx.AsyncClient() as client:
        try:
            # Giving it a generous 45-second timeout since it browses and parses live
            response = await client.post(endpoint, json=payload, headers=headers, timeout=45.0)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Successfully extracted insights for {company_url}")
                return data # This will contain the structured response text from Haunt!
            else:
                logger.warning(f"Haunt API returned status code: {response.status_code}. Response: {response.text}")
                # TODO: Trigger your old BeautifulSoup fallback function here if needed!
                return {"error": "Failed to extract data from Haunt API"}

        except httpx.TimeoutException:
            logger.error(f"Haunt API timed out while trying to scrape {company_url}")
            return {"error": "Extraction timed out"}
        except Exception as e:
            logger.error(f"Unexpected error during Haunt API extraction: {str(e)}")
            return {"error": "An unexpected error occurred"}
        
#Manual scraping if HauntAPI token out
def scrape_website(url: str) -> str:
    """
    Takes a company website URL, safely fetches the HTML content,
    and returns a clean string of the first few paragraphs.
    """
    # A standard User-Agent header to mimic a regular browser visit
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        # Fetch the webpage with a 5-second timeout so the system doesn't hang forever
        response = requests.get(url, headers=headers, timeout=5)
        
        # SimplifIQ values handling real-world scenarios gracefully!
        # If the response isn't successful (e.g., 404, 403, 500), we exit cleanly.
        if response.status_code != 200:
            print(f"[Scraper] Warning: Received status code {response.status_code} for {url}")
            return ""
            
        # Parse the raw HTML text
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find all paragraph tags
        paragraphs = soup.find_all("p")
        
        # Extract, clean, and combine the text of the first 5 paragraphs
        collected_text = []
        for p in paragraphs[:5]:
            cleaned_text = p.text.strip()
            if cleaned_text:  # Only add if the paragraph isn't empty spaces
                collected_text.append(cleaned_text)
                
        # Join the list into a single coherent block of text
        return " ".join(collected_text)
        
    except Exception as e:
        # If the website is totally down or blocks our script completely,
        # we log the error and return an empty string instead of crashing the pipeline.
        print(f"[Scraper] Error scraping {url}: {e}")
        return ""