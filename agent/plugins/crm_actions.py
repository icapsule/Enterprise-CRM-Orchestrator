import os
from langchain_core.tools import tool

@tool
def schedule_crm_followup_task(lead_name: str, task_title: str, due_date: str) -> str:
    """
    Schedule a follow-up task or event in the CRM (Salesforce/HubSpot) for a specific lead.
    Use this tool ONLY when the user asks to schedule, follow up, create a task, or set a reminder for a lead.
    
    Args:
        lead_name: The name of the lead (e.g., 'Johan Nilsson').
        task_title: The descriptive title of the task (e.g., 'Send Ericsson B2B Customized Proposal').
        due_date: The date the task is due (e.g., '2026-07-08' or 'next Monday').
    """
    # High-fidelity mock representation of an authenticated POST request to CRM Tasks API
    # e.g., POST https://api.hubapi.com/crm/v3/objects/tasks
    
    return (
        f"[CRM Action Success] Scheduled task in CRM for lead '{lead_name}':\n"
        f"  - Task Title: '{task_title}'\n"
        f"  - Due Date: {due_date}\n"
        f"  - Status: Placed in Sales Queue (Pending Assigned Rep Confirmation)"
    )

@tool
def send_slack_alert(channel: str, message: str) -> str:
    """
    Send an instant notification alert to a specific team Slack channel.
    Use this tool ONLY when the user asks to send an alert, warn the team, notify Slack, or alert channels.
    
    Args:
        channel: The Slack channel name starting with '#' (e.g., '#sales-alerts', '#sales-vip').
        message: The alert message body.
    """
    # High-fidelity mock representation of a webhook POST to Slack
    # e.g., POST https://hooks.slack.com/services/YOUR_WORKSPACE/YOUR_WEBHOOK_URL
    
    return (
        f"[Slack Notification Success] Alert pushed to Slack channel '{channel}':\n"
        f"  - Payload: {message}\n"
        f"  - Webhook Status: 200 OK"
    )
