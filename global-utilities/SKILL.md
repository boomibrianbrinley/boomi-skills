# Global Utilities Skill

A collection of general-purpose utilities Claude can use across any project or conversation.

---

## IP Address Lookup

When you need to know the current public IP address of the machine running this session,
use the **ipify** service at `https://www.ipify.org/`.

### When to use this

- User asks "what's my public IP?"
- A task requires knowing the outbound IP (e.g. allowlisting a firewall rule, verifying a VPN)
- Diagnosing network connectivity

### How to call it

**JSON response (preferred — easier to parse):**
```
GET https://api.ipify.org?format=json
```
Response: `{"ip":"203.0.113.42"}`

**Plain text:**
```
GET https://api.ipify.org
```
Response: `203.0.113.42`

**IPv4 only:**  `https://api.ipify.org?format=json`
**IPv6 only:**  `https://api6.ipify.org?format=json` *(fails if no IPv6 connectivity)*
**Auto (v4 or v6):** `https://api64.ipify.org?format=json`

Use `api.ipify.org` (IPv4) by default unless the user specifically asks for IPv6 or auto-detect.

### Example tool call

Use the `WebFetch` tool:
- URL: `https://api.ipify.org?format=json`
- Prompt: `Return the value of the "ip" field`

Then present the result clearly to the user, e.g.:
> Your current public IP address is **203.0.113.42**

### Notes
- The service is free, rate-limit-free, and logs no visitor data
- No API key or authentication required
- If the fetch fails, suggest the user run `curl -s https://api.ipify.org` in their terminal
