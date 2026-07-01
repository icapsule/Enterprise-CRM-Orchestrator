import os
import json
from langchain_core.tools import tool

@tool
def fetch_salesforce_leads() -> str:
    """
    Fetch the most recent B2B leads from Salesforce CRM.
    Use this tool ONLY when the user explicitly asks about Salesforce leads, prospects, pipeline values, or Swedish B2B clients.
    """
    # High-fidelity mock B2B leads representing Swedish/Nordic enterprise clients
    # Includes properties critical for pipeline analysis: Budget, Status, Country, Source, Owner
    mock_leads = [
        {
            "name": "Lars Andersson", 
            "email": "lars.andersson@volvo.com",
            "company": "Volvo Group", 
            "country": "Sweden",
            "status": "Hot Lead", 
            "estimated_value": 250000, 
            "source": "Web Inquiry",
            "owner": "Sven Lindberg"
        },
        {
            "name": "Elin Bergqvist", 
            "email": "elin.b@spotify.se",
            "company": "Spotify AB", 
            "country": "Sweden",
            "status": "Working", 
            "estimated_value": 180000, 
            "source": "Referral",
            "owner": "Anna Sjöberg"
        },
        {
            "name": "Johan Nilsson", 
            "email": "johan.nilsson@ericsson.se",
            "company": "Ericsson", 
            "country": "Sweden",
            "status": "Hot Lead", 
            "estimated_value": 420000, 
            "source": "Cold Outreach",
            "owner": "Sven Lindberg"
        },
        {
            "name": "Karin Ekdahl", 
            "email": "karin.ekdahl@ikea.com",
            "company": "IKEA", 
            "country": "Sweden",
            "status": "Nurturing", 
            "estimated_value": 95000, 
            "source": "Stockholm Event",
            "owner": "Erik Larson"
        },
        {
            "name": "Sven Larsson", 
            "email": "sven.larsson@hm.se",
            "company": "H&M Group", 
            "country": "Sweden",
            "status": "Cold Lead", 
            "estimated_value": 50000, 
            "source": "Web Inquiry",
            "owner": "Anna Sjöberg"
        },
        {
            "name": "Sofia Lindqvist", 
            "email": "sofia.l@klarna.com",
            "company": "Klarna Bank", 
            "country": "Sweden",
            "status": "Hot Lead", 
            "estimated_value": 300000, 
            "source": "Partner Referral",
            "owner": "Erik Larson"
        },
        {
            "name": "Anders Holm", 
            "email": "anders.holm@sandvik.se",
            "company": "Sandvik", 
            "country": "Sweden",
            "status": "Qualified", 
            "estimated_value": 150000, 
            "source": "Webinar",
            "owner": "Sven Lindberg"
        },
        {
            "name": "Emma Sjöberg", 
            "email": "emma.sjoberg@scania.se",
            "company": "Scania", 
            "country": "Sweden",
            "status": "Hot Lead", 
            "estimated_value": 220000, 
            "source": "Inbound call",
            "owner": "Anna Sjöberg"
        },
        {
            "name": "Jonas Wallin", 
            "email": "jonas.wallin@electrolux.se",
            "company": "Electrolux AB", 
            "country": "Sweden",
            "status": "Working", 
            "estimated_value": 80000, 
            "source": "Referral",
            "owner": "Erik Larson"
        },
        {
            "name": "Astrid Lindgren", 
            "email": "astrid.l@vattenfall.se",
            "company": "Vattenfall", 
            "country": "Sweden",
            "status": "Nurturing", 
            "estimated_value": 130000, 
            "source": "Conference",
            "owner": "Sven Lindberg"
        }
    ]
    
    return json.dumps(mock_leads, ensure_ascii=False)
