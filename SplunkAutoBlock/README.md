\## Overview

Built a hands-on SOC (Security Operations Center) lab that detects brute-force login attempts and automatically blocks attacker IPs in real time using Splunk, Python, and PowerShell.



\---



\## Architecture



Kali Linux (Attacker)  

↓ SMB / RDP Brute Force  

Windows 10 (Victim) → Splunk Universal Forwarder  

↓ Windows Security Logs  

Windows 11 (Defender) → Splunk Enterprise  

↓ Alert Triggered  

Python Listener → PowerShell → Firewall Block ✅  



\---



\## 🛠 Setup (Step-by-Step)



\### 1. Place Scripts



C:\\SplunkAutoBlock\\





\### 2. Enable PowerShell Execution



Set-ExecutionPolicy RemoteSigned





\### 3. Allow Listener Port



New-NetFirewallRule -DisplayName "SplunkListener8888" -Direction Inbound -Protocol TCP -LocalPort 8888 -Action Allow





\### 4. Run Python Listener



python listener.py





(Optional: Register as Scheduled Task for auto-start)



\### 5. Configure Splunk Alert

\- Condition: count > 3  

\- Trigger: For each result  

\- Action: Webhook  

\- URL: http://localhost:8888  



\---



\## 🔍 Detection Logic



```spl

index=\* EventCode=4625

| stats count by Source\_Network\_Address

| where count > 3

| rename Source\_Network\_Address as src\_ip

| table src\_ip, count

