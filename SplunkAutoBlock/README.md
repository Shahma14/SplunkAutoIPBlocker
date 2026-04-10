# 🔐 Splunk Automated IP Blocker — SOC Home Lab

## Overview
A real-time SOC lab that detects brute force attacks and automatically blocks attacker IPs using Splunk, Python, and PowerShell — with zero manual intervention.

---

## Architecture

Kali Linux (Attacker)  
↓ SMB Brute Force  
Windows 10 (Victim) → Splunk Forwarder  
↓ Event Logs  
Windows 11 (Defender) → Splunk Enterprise  
↓ Alert Triggered  
Python Listener → PowerShell → Firewall Block ✅  

---

## Tools Used
- Splunk Enterprise + Universal Forwarder  
- Python 3  
- PowerShell  
- Windows Defender Firewall  
- Kali Linux / CrackMapExec  
- VirtualBox  

---

## Detection Query

```spl
index=* EventCode=4625
| stats count by Source_Network_Address
| where count > 3
| rename Source_Network_Address as src_ip
| table src_ip, count

## How It Works

1.Kali attacks Windows 10 via SMB brute force
2.Windows generates EventCode 4625 (failed login) logs
3.Splunk detects pattern and fires webhook alert
4.Python listener receives alert and extracts attacker IP
5.PowerShell blocks IP via Windows Firewall automatically
6.Attacker connection drops mid-attack ✅

## Setup

1.Clone this repo
2.Place scripts in:
C:\SplunkAutoBlock\
3.Enable PowerShell:
Set-ExecutionPolicy RemoteSigned
4.Register listener as Scheduled Task
5.Configure Splunk Alert:
Condition: count > 3
Action: Webhook
URL: http://localhost:8888


## ⚡ PowerShell Commands Used

*Enable PowerShell Script Execution
Set-ExecutionPolicy RemoteSigned

*Create Firewall Rule to Allow Listener
New-NetFirewallRule -DisplayName "SplunkListener8888" -Direction Inbound -Protocol TCP -LocalPort 8888 -Action Allow

*Block Attacker IP (Executed Automatically)
New-NetFirewallRule -DisplayName "SPLUNK_BLOCK_<IP>" -Direction Inbound -RemoteAddress <IP> -Action Block

*Verify Blocked IPs
Get-NetFirewallRule | findstr SPLUNK_BLOCK

*Unblock IP
Remove-NetFirewallRule -DisplayName "SPLUNK_BLOCK_<IP>"

### Results
Detected brute force attack in real time
Blocked attacker IP automatically mid-attack
Full audit trail in blocked_ips.log
