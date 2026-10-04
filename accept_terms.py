import requests
import json

# Insert your secure API key here
API_KEY = "YOUR_EVREN_API_KEY_HERE"

# Base URL as per documentation
BASE_URL = "https://evren-llmapi.ssyz.org.tr/v1"

# Required headers (Note the use of X-API-Key as per docs)
HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

def accept_evren_terms():
    print("[*] Checking terms of service acceptance status...")
    
    # 1. Fetch terms status and current version
    status_url = f"{BASE_URL}/terms/status"
    try:
        status_response = requests.get(status_url, headers={"X-API-Key": API_KEY})
        
        if status_response.status_code == 200:
            status_data = status_response.json()
            is_accepted = status_data.get("accepted", False)
            current_version = status_data.get("current_version", 1)
            
            if is_accepted:
                print("[+] Terms are already accepted. No further action needed!")
                return
            else:
                print(f"[-] Terms not accepted. Sending acceptance for version: {current_version}...")
                
                # 2. Send acceptance request
                accept_url = f"{BASE_URL}/terms/accept"
                payload = {"version": current_version}
                
                accept_response = requests.post(accept_url, headers=HEADERS, data=json.dumps(payload))
                
                if accept_response.status_code == 200:
                    print("[+] Terms accepted successfully! You can now run the Context-Breaker tool.")
                    print("Response details:", accept_response.json())
                else:
                    print(f"[!] Error during acceptance: {accept_response.status_code}")
                    print(accept_response.text)
        else:
            print(f"[!] Failed to fetch terms status: {status_response.status_code}")
            print(status_response.text)
            
    except Exception as e:
        print(f"[!] Connection error: {e}")

if __name__ == "__main__":
    accept_evren_terms()
