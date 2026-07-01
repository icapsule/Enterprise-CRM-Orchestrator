import os
import json
from langchain_core.tools import tool

@tool
def fetch_salesforce_leads() -> str:
    """
    Fetch the most recent leads from Salesforce CRM.
    Use this tool ONLY when the user explicitly asks about leads, prospects, or Salesforce data.
    """
    # In a real scenario, this would authenticate using SF_CLIENT_ID and SF_CLIENT_SECRET
    # and execute an SOQL query via the Salesforce REST API.
    
    # For this demonstration, we return mock enterprise data to prove cross-system extensibility
    mock_leads = [
        {"name": "Alice Wonderland", "company": "TechCorp Inc.", "status": "Hot Lead"},
        {"name": "Bob Builder", "company": "Construction LLC", "status": "Cold Lead"}
    ]
    
    leads_str = ", ".join([f"{l['name']} from {l['company']} ({l['status']})" for l in mock_leads])
    
    return f"Recent Salesforce Leads: {leads_str}"
