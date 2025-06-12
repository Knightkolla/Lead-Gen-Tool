import os
from typing import Dict, Any
import google.generativeai as genai

# Placeholder for Gemini API integration
# In a real application, you would initialize the Gemini client here
# For example: import google.generativeai as genai
# genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def get_company_insights(company_data: Dict[str, Any]) -> Dict[str, str]:
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        print("Warning: GEMINI_API_KEY not set. Using dummy insights data.")
        company_name = company_data.get("name", "a company")
        industry = company_data.get("industry", "its industry")
        location = company_data.get("location", "its location")
        return {
            "insightsSummary": f"Insights for {company_name}: This company operates in the {industry} sector, located in {location}. Further AI-powered insights require a configured GEMINI_API_KEY."
        }

    try:
        genai.configure(api_key=gemini_api_key)
        
        # List available models
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Model: {m.name}")
        
        model = genai.GenerativeModel('gemini-1.5-flash')

        company_name = company_data.get("name", "")
        industry = company_data.get("industry", "")
        location = company_data.get("location", "")
        website = company_data.get("website", "")
        description = company_data.get("description", "")
        employee_count = company_data.get("employeeCount", "")
        revenue = company_data.get("revenue", "")

        prompt = f"""
        As a B2B sales intelligence expert, analyze this company and provide a concise, actionable summary:

        Company Details:
        - Name: {company_name}
        - Industry: {industry}
        - Location: {location}
        - Size: {employee_count} employees
        - Revenue: {revenue}
        - Website: {website}
        - Description: {description}

        Please provide a brief analysis that includes:
        1. Key business strengths and unique selling points
        2. Potential growth opportunities
        3. Market position and competitive advantages
        4. Specific sales outreach recommendations

        Keep the response concise, professional, and focused on actionable insights for B2B sales.
        """
        
        response = model.generate_content(prompt)
        insights_summary = response.text
        return {"insightsSummary": insights_summary}
    except Exception as e:
        print(f"Error generating insights with Gemini API: {e}")
        return {
            "insightsSummary": "Failed to generate AI-powered insights due to an error: " + str(e) + ". Please ensure your GEMINI_API_KEY is valid and the API is accessible."
        } 