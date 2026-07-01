from .hubspot import fetch_hubspot_contacts
from .salesforce import fetch_salesforce_leads

# Centralized Plugin Registry
# In the future, this can be refactored to dynamically scan the plugins directory
ALL_TOOLS = [
    fetch_hubspot_contacts,
    fetch_salesforce_leads
]
