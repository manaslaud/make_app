import requests
import json

def add_lead_to_google_sheets(doc, method):
    # Your Make webhook URL
    make_webhook_url = "https://hook.us1.make.com/ehxg0vqbamtsodarymqjll60g96myd7c"

    # Data to send to Make (this is the data structure)
    data = {
        "lead_name": doc.lead_name,
        "email_id": doc.email_id,
        "company_name": doc.company_name,
        "status": doc.status
    }

    # Log the data structure to the ERPNext logs
    print("Sending data to Make:")
    print(json.dumps(data, indent=4))  # Pretty print for easy reading

    # Send data to Make via webhook
    response = requests.post(make_webhook_url, json=data)
    if response.status_code == 200:
        print("Lead data sent to Make successfully!")
    else:
        print(f"Failed to send lead data: {response.text}")
