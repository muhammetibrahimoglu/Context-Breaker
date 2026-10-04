# Context-Breaker

Context-Breaker is an AI-powered Automated API Security Scanner designed to detect complex Business Logic Flaws and Broken Object Level Authorization (BOLA/IDOR) vulnerabilities in HTTP logs. 

Traditional WAFs and IDS/IPS systems often fail to detect logic-based API attacks because the HTTP requests appear structurally valid. Context-Breaker solves this by leveraging Large Language Models (LLMs) to deeply analyze the *context* and *intent* of the request.

## Features
- **Automated Log Analysis:** Parses bulk HTTP requests from log files.
- **Business Logic Detection:** Identifies IDOR/BOLA, authorization bypasses, and OTP logic flaws.
- **MITRE ATT&CK Mapping:** Automatically maps detected threats to specific MITRE ATT&CK techniques (e.g., T1190, T1098).
- **Proactive Defense (YARA):** Generates precise YARA rules for immediate integration into SIEM/SOC workflows.
- **Privacy-First Inference:** Utilizes the EVREN LLM API to ensure data sovereignty and secure API communication.
- **Proof of Concept (PoC):** Currently demonstrates sequential log analysis. The future roadmap includes asynchronous multi-threading to process large-scale production logs simultaneously.

## Prerequisites
- Python 3.7+
- `openai` and `requests` libraries
- Valid API Key from the EVREN LLM Platform

## Installation & Usage

> **Note:** If this is your first time using the EVREN API, please run `python3 accept_terms.py` once to accept the LLM terms of service before running the main scanner.

1. Clone the repository:
```bash
git clone https://github.com/muhammetibrahimoglu/Context-Breaker.git
cd Context-Breaker
```

2. Set up an isolated virtual environment (Recommended):

```bash
python3 -m venv context_env
source context_env/bin/activate
pip install openai requests
```

3. Add your secure EVREN API Key inside `context_breaker.py`.
4. Place your intercepted HTTP requests in `api_logs.txt` (separate each request with `###`).
5. Run the automated scanner:

```bash
python3 context_breaker.py
```

## Case Study

This tool was successfully tested against a real-world BOLA/Account Takeover vulnerability pattern involving `user_id` manipulation in a `/change_email` API endpoint. It successfully identified the anomaly, mapped it to MITRE T1190, and generated defensive YARA rules without false positives on legitimate traffic.
