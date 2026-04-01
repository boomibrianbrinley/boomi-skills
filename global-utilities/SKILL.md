# Global Utilities Skill

A collection of general-purpose utilities Claude can use across any project or conversation.

---

## 1. Public IP Address Lookup

When you need to know the current public IP address of the machine running this session,
use the **ipify** service at `https://www.ipify.org/`.

### When to use this
- User asks "what's my public IP?"
- A task requires knowing the outbound IP (e.g. allowlisting a firewall rule, verifying a VPN)
- Diagnosing network connectivity

### How to call it

**JSON response (preferred):**
```
GET https://api.ipify.org?format=json
```
Response: `{"ip":"203.0.113.42"}`

**Variants:**
- IPv4 only: `https://api.ipify.org?format=json`
- IPv6 only: `https://api6.ipify.org?format=json` *(fails if no IPv6 connectivity)*
- Auto (v4 or v6): `https://api64.ipify.org?format=json`

Use `api.ipify.org` (IPv4) by default unless the user asks for IPv6 or auto-detect.

### Example tool call
Use the `WebFetch` tool:
- URL: `https://api.ipify.org?format=json`
- Prompt: `Return the value of the "ip" field`

Present result as: *Your current public IP address is **203.0.113.42***

### Fallback
If WebFetch is unavailable: `curl -s https://api.ipify.org`

### Notes
- Free, rate-limit-free, logs no visitor data. No API key required.

---

## 2. Current Date and Time

When you need a precise current timestamp (not just today's date), use **timeapi.io**.

### When to use this
- User asks "what time is it?" or needs a precise timestamp
- Generating report headers, log entries, or file names that require the current time
- Checking what time it is in a specific timezone

### How to call it

**Current UTC time:**
```
GET https://timeapi.io/api/v1/time/current/utc
```
Response fields: `dateTime`, `date`, `time`, `timeZone`, `dstActive`

Example response:
```json
{
  "dateTime": "2024-03-15T14:32:07.123456",
  "date": "03/15/2024",
  "time": "14:32",
  "timeZone": "UTC",
  "dstActive": false
}
```

**Time in a specific timezone:**
```
GET https://timeapi.io/api/v1/time/current/zone?timezone=America/New_York
```
Use IANA timezone names (e.g. `America/Chicago`, `Europe/London`, `Asia/Tokyo`).

**Unix timestamp only:**
```
GET https://timeapi.io/api/v1/time/current/unix
```
Returns seconds since 1970-01-01 UTC.

### Example tool call
Use the `WebFetch` tool:
- URL: `https://timeapi.io/api/v1/time/current/utc`
- Prompt: `Return the dateTime and timeZone fields`

Present result as: *Current UTC time is **2024-03-15 14:32:07***

### Fallback
If WebFetch is unavailable: `date -u` (macOS/Linux) or `Get-Date -AsUTC` (PowerShell)

### Notes
- Free tier available. No API key required for basic time queries.
- Use IANA timezone names, not abbreviations (e.g. `America/New_York` not `EST`).

---

## 3. DNS Lookup

When you need to resolve DNS records for a domain, use **Google's DNS-over-HTTPS API**.

### When to use this
- User asks "what IP does example.com resolve to?"
- Verifying DNS propagation after a config change
- Checking MX records for email routing
- Diagnosing connectivity issues

### How to call it

**Base URL:** `https://dns.google/resolve`

**Query parameters:**
- `name` (required) — domain name to look up
- `type` (optional, default `A`) — record type: `A`, `AAAA`, `MX`, `TXT`, `CNAME`, `NS`, `SOA`

**A record (IPv4 address):**
```
GET https://dns.google/resolve?name=example.com&type=A
```

**MX record (mail servers):**
```
GET https://dns.google/resolve?name=example.com&type=MX
```

**TXT record (SPF, DKIM, domain verification):**
```
GET https://dns.google/resolve?name=example.com&type=TXT
```

**Response structure:**
```json
{
  "Status": 0,
  "Question": [{"name": "example.com.", "type": 1}],
  "Answer": [
    {"name": "example.com.", "type": 1, "TTL": 3600, "data": "93.184.216.34"}
  ]
}
```
- `Status: 0` = NOERROR (success); `Status: 3` = NXDOMAIN (not found)
- `Answer` array contains one entry per record; `data` field holds the value
- `type` numbers: 1=A, 28=AAAA, 15=MX, 16=TXT, 5=CNAME, 2=NS

### Example tool call
Use the `WebFetch` tool:
- URL: `https://dns.google/resolve?name=example.com&type=A`
- Prompt: `Return the Status and all entries in the Answer array, showing name, TTL, and data for each`

### Fallback
If WebFetch is unavailable: `nslookup example.com` or `dig example.com A`

### Notes
- No API key required. Publicly available.
- Responses use DNSSEC validation by default.
- Domain names in the response include a trailing dot (e.g. `example.com.`) — this is normal.

---

## 4. SSL Certificate Check

When you need to verify a site's SSL certificate (expiry date, issuer, validity), use
**`openssl` via bash** as the primary method, with **SSL Labs API** as an alternative
when a full TLS grade is needed.

### When to use this
- User asks "when does the SSL cert expire for example.com?"
- Checking if a cert is valid before going live
- Diagnosing SSL handshake errors
- Getting a full TLS security grade for a domain

### Method A — Bash (fastest, returns expiry + issuer directly)

```bash
echo | openssl s_client -servername example.com -connect example.com:443 2>/dev/null \
  | openssl x509 -noout -dates -subject -issuer
```

Output:
```
notBefore=Jan  1 00:00:00 2024 GMT
notAfter=Jan  1 00:00:00 2025 GMT
subject=CN=example.com
issuer=C=US, O=Let's Encrypt, CN=R3
```

For a non-standard port: replace `443` with the actual port.

### Method B — SSL Labs API (full TLS grade, slower)

SSL Labs runs a full assessment — this can take 60–90 seconds for a new host.
Use it when the user wants a grade (A+/A/B/F) or detailed TLS configuration analysis.

**Start or retrieve a cached assessment:**
```
GET https://api.ssllabs.com/api/v3/analyze?host=example.com&fromCache=on&maxAge=24
```
Parameters:
- `fromCache=on&maxAge=24` — return cached result if assessed within last 24 hours (much faster)
- `startNew=on` — force a fresh assessment (slow, use only if user explicitly wants fresh data)

**Response `status` field:**
- `"READY"` — assessment complete, read `endpoints[].grade`
- `"IN_PROGRESS"` — still running, poll again in 10–15 seconds
- `"ERROR"` — assessment failed

**Grades:** A+ → A → B → C → D → E → F (F = serious issues)

**Rate limits:** Max 7 concurrent assessments, 1 second between new requests.

### Fallback
If neither openssl nor WebFetch is available:
- Suggest user visit `https://www.ssllabs.com/ssltest/analyze.html?d=example.com`
- Or: `curl -vI https://example.com 2>&1 | grep -A5 "Server certificate"`

### Notes
- `openssl` is available on macOS and most Linux distros by default. On Windows, use Git Bash or WSL.
- SSL Labs results are cached publicly — results for popular domains are usually instant.
- For internal/private hostnames not reachable from the internet, only Method A (bash) will work.
