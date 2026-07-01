import os
import requests
from langchain_core.tools import tool

@tool
def fetch_hubspot_contacts() -> str:
    """
    Fetch the most recent contacts from HubSpot CRM.
    Use this tool ONLY when the user explicitly asks about contacts or customers in HubSpot.
    """
    token = os.getenv("HUBSPOT_ACCESS_TOKEN")
    if not token:
        return "Error: HUBSPOT_ACCESS_TOKEN not found in environment."

    url = "https://api.hubapi.com/crm/v3/objects/contacts?limit=5&properties=firstname,lastname,email"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        # Commercial Graceful Fallback
        if response.status_code != 200:
            return f"System Integration Warning: HubSpot API returned status {response.status_code}. Detail: {response.text}"
        
        data = response.json()
        contacts = []
        for result in data.get('results', []):
            props = result.get('properties', {})
            name = f"{props.get('firstname', '')} {props.get('lastname', '')}".strip()
            email = props.get('email', 'No Email')
            contacts.append(f"{name} ({email})")
            
        if not contacts:
            return "No contacts found in HubSpot."
            
        return "Recent HubSpot Contacts: " + ", ".join(contacts)
    
    except requests.exceptions.RequestException as e:
        return f"System Integration Warning: Failed to connect to HubSpot. Error: {str(e)}"
