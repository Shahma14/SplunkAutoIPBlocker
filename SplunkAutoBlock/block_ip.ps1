param(
    [string]$ip
)

# Validate IP format
if ($ip -notmatch '^\d{1,3}(\.\d{1,3}){3}$') {
    Write-Output "Invalid IP: $ip"
    exit 1
}

# Skip if already blocked
$exists = Get-NetFirewallRule -DisplayName "SPLUNK_BLOCK_$ip" -ErrorAction SilentlyContinue
if ($exists) {
    Write-Output "Already blocked: $ip"
    exit 0
}

# Block inbound
New-NetFirewallRule `
    -DisplayName "SPLUNK_BLOCK_$ip" `
    -Direction Inbound `
    -Action Block `
    -RemoteAddress $ip `
    -Protocol Any `
    -Enabled True `
    -Description "Auto-blocked by Splunk on $(Get-Date)"

# Block outbound
New-NetFirewallRule `
    -DisplayName "SPLUNK_BLOCK_OUT_$ip" `
    -Direction Outbound `
    -Action Block `
    -RemoteAddress $ip `
    -Protocol Any `
    -Enabled True `
    -Description "Auto-blocked by Splunk on $(Get-Date)"

# Log to a text file
$logLine = "$(Get-Date) - BLOCKED: $ip"
Add-Content -Path "C:\SplunkAutoBlock\blocked_ips.log" -Value $logLine

Write-Output "Blocked: $ip"