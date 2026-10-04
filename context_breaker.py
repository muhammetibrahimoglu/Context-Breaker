from openai import OpenAI
import sys
import os

# 1. Connection Settings
API_KEY = "YOUR_EVREN_API_KEY_HERE"
BASE_URL = "https://evren-llmapi.ssyz.org.tr/v1"

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

system_prompt = """
You are an expert Blue Team API Security Analyst. 
I will provide you with an intercepted HTTP request log. Your task is to:
1. Analyze the context to detect Business Logic Flaws and authorization manipulation (e.g., IDOR/BOLA).
2. If NO vulnerability is found, simply reply with "SECURE: No business logic flaws detected." and stop.
3. If a vulnerability is found, explain the mechanics, map it to the exact MITRE ATT&CK technique, and generate a YARA rule.
Provide the output in a clean, structured security report format.
"""

# 2. Read Log File
log_file_path = "api_logs.txt"

if not os.path.exists(log_file_path):
    print(f"[-] Error: Log file '{log_file_path}' not found.")
    sys.exit(1)

with open(log_file_path, "r") as file:
    raw_logs = file.read()

# Split logs based on the delimiter
requests_list = [req.strip() for req in raw_logs.split("###") if req.strip()]

print(f"[*] Context-Breaker Engine Initialized...")
print(f"[*] Found {len(requests_list)} HTTP requests in {log_file_path}. Starting analysis...\n")

# 3. Analyze requests one by one
for index, req in enumerate(requests_list, 1):
    print("=" * 60)
    print(f"[*] Analyzing Request #{index}...")
    print("-" * 60)
    
    try:
        stream = client.chat.completions.create(
            model="deepseek-v4.1-flash",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze this request:\n{req}"}
            ],
            max_tokens=4096,
            stream=True
        )

        for chunk in stream:
            delta = chunk.choices[0].delta if chunk.choices else None
            if not delta:
                continue
            
            # Mute model reasoning (Chain of Thought)
            reasoning = getattr(delta, "reasoning", None) or getattr(delta, "reasoning_content", None)
            if reasoning:
                pass 
                
            # Print final output
            if delta.content:
                print(delta.content, end="", flush=True)
                
        print("\n")
        
    except Exception as e:
        print(f"\n[-] Execution Error on Request #{index}: {e}")

print("\n[+] Batch Analysis Completed Successfully.")
