from .hubspot import fetch_hubspot_contacts
from .salesforce import fetch_salesforce_leads
from .crm_actions import schedule_crm_followup_task, send_slack_alert

# Centralized Plugin Registry
ALL_TOOLS = [
    fetch_hubspot_contacts,
    fetch_salesforce_leads,
    schedule_crm_followup_task,
    send_slack_alert
]
