import os
from groq import Groq
import httpx

def generate_insights(company_name: str, scraped_context: str) -> str:
    """
    Connects to Groq cloud API using Llama-3 to generate 3 custom, 
    highly tailored business optimization insights.
    """
    # 1. Fetch the API key safely from the system environment
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("[AI Engine] Error: GROQ_API_KEY not found in environment variables.")
        return "Fallback Insight: Focus on automating customer acquisition channels and optimizing core operational workflows."

    try:
        # 2. Initialize the Groq Client
        client = Groq(
            api_key=api_key,
            http_client=httpx.Client()
        )
        # ---------------------------------
        
        # 3. Handle real-world limitations (Sensible Fallbacks)
        # If the scraper found text, we give it to the AI. If not, we adjust the instructions.
        if scraped_context:
            system_instruction = "You are an elite B2B sales strategist and business consultant."
            user_prompt = f"""
            Analyze this raw website data collected from the company '{company_name}':
            ---
            {scraped_context}
            ---
            Based on this data, provide exactly 3 highly specific, professional, and actionable digital or operational insights/improvements for them. 
            Do not use markdown bolding (**) or bullet symbols (* or -) in the text response. Keep it clean and readable for a PDF layout.
            """
        else:
            # Fallback prompt if scraping failed
            system_instruction = "You are an expert industry analyst."
            user_prompt = f"""
            We tried to analyze the company '{company_name}' but their website was unreachable. 
            Assuming they operate as a standard B2B services or software company, provide 3 general industry best-practice optimizations they should focus on.
            Do not use markdown bolding (**) or bullet symbols in the text response. Keep it clean and readable for a PDF layout.
            """

        # 4. Request completion from Llama-3
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.1-8b-instant",  # Updated to the active production model ID
            temperature=0.7,
            max_tokens=500
        )

        # Extract and return the text output
        return chat_completion.choices[0].message.content.strip()

    except Exception as e:
        # Final safety fallback if Groq API goes down or rate limits us
        print(f"[AI Engine] Groq API exception caught: {e}")
        return "1. Digital Workflow Enhancement: Streamline client intake steps.\n2. Technical Optimization: Audit application layer bottlenecks.\n3. Operational Scale: Deploy automated messaging channels."