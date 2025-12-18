import httpx
from config import AT_USERNAME, AT_API_KEY, AT_SMS_FROM

async def send_sms_alert(phone: str, message: str):
    if not AT_API_KEY:
        print(f"[Mock SMS to {phone}]: {message}")
        return

    base_url = "https://api.sandbox.africastalking.com/version1/messaging" if AT_USERNAME == "sandbox" else "https://api.africastalking.com/version1/messaging"
    
    headers = {"apiKey": AT_API_KEY, "Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "username": AT_USERNAME,
        "to": phone,
        "message": message,
        "from": AT_SMS_FROM
    }

    async with httpx.AsyncClient() as client:
        await client.post(base_url, headers=headers, data=payload)