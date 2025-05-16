import requests
import json
import frappe

# later MAKE_WEBHOOK_URL TO BE HARDCODED AS MAKE_CUSTOM_APP'S WEBHOOK URL AND ROUTING BASED ON api keys for each  client 
# sending api key's and client keys in header to identify which client is using it

def add_lead(doc, method):

    make_webhook_url = "https://hook.us1.make.com/ehxg0vqbamtsodarymqjll60g96myd7c"

    data = {
        "lead_name": doc.lead_name,
        "email_id": doc.email_id,
        "company_name": doc.company_name,
        "status": doc.status
    }

    # Log the data structure to the ERPNext logs
    print("Sending data to Make:")
    print(json.dumps(data, indent=4)) 

    # Send data to Make via webhook
    response = requests.post(make_webhook_url, json=data)
    if response.status_code == 200:
        print("Lead data sent to Make successfully!")
    else:
        print(f"Failed to send lead data: {response.text}")

def add_sales_order(doc, method):
    make_webhook_url ="https://hook.us1.make.com/ehxg0vqbamtsodarymqjll60g96myd7c"

    data = {
        "customer": doc.customer,
        "transaction_date": str(doc.transaction_date),
        "grand_total": doc.grand_total,
        "status": doc.status,
        "sales_order_id": doc.name
    }

    print("Sending Sales Order data to Make:")
    print(json.dumps(data, indent=4))

    # Send to Make
    response = requests.post(make_webhook_url, json=data)
    if response.status_code == 200:
        print("Sales Order sent to Make successfully!")
    else:
        print(f"Failed to send sales order: {response.text}")


def on_lead_created(doc, method):
    frappe.logger().info(f"New Lead Created: {doc.name}, Email: {doc.email_id}")

    payload = {
        "name": doc.lead_name,
        "email": doc.email_id,
        "phone": doc.phone,
        "company": doc.company_name,
        "source": doc.source
    }

    try:
        response = requests.post("https://hook.us1.make.com/ehxg0vqbamtsodarymqjll60g96myd7c", json=payload)
        response.raise_for_status()
        frappe.logger().info(f"Webhook success: {response.text}")
    except Exception as e:
        frappe.log_error(f"Webhook failed: {str(e)}", "MakeApp Lead Webhook Error")


def send_purchase_order_to_make(doc, method):
    data = {
        "doctype": "Purchase Order",
        "name": doc.name,
        "data": doc.as_dict()
    }

    webhook_url = "https://hook.make.com/your-purchase-order-webhook-url"

    try:
        res = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
        res.raise_for_status()
        frappe.logger().info(f"[MAKE WEBHOOK SUCCESS] Purchase Order: {doc.name}")
    except Exception as e:
        frappe.log_error(f"Failed to send Purchase Order {doc.name} to Make webhook\nError: {str(e)}", "Webhook Error")


def send_purchase_invoice_to_make(doc, method):
    data = {
        "doctype": "Purchase Invoice",
        "name": doc.name,
        "data": doc.as_dict()
    }

    webhook_url = "https://hook.make.com/your-purchase-invoice-webhook-url"  

    try:
        res = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
        res.raise_for_status()
        frappe.logger().info(f"[MAKE WEBHOOK SUCCESS] Purchase Invoice: {doc.name}")
    except Exception as e:
        frappe.log_error(f"Failed to send Purchase Invoice {doc.name} to Make webhook\nError: {str(e)}", "Webhook Error")
