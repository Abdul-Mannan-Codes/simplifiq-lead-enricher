import requests
from bs4 import BeautifulSoup

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