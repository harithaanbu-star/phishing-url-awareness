# Test Results

Python version used: 3.14.6 | Operating system: Windows 11 | Date: 2026-10-27

| # | Input | Expected result | Actual result | Pass/Fail |
|---|-------|-----------------|---------------|-----------|
| 1 | `https://www.example.com/login` | No listed warning signs | No listed warning signs found. This does NOT prove safety. | PASS |
| 2 | `http://192.0.2.10/account` | IP address + HTTP | Uses an IP address instead of a familiar domain.<br>Uses HTTP. HTTPS alone does not prove trust. | PASS |
| 3 | `http://example.com@sample.invalid/login` | @ symbol + HTTP | Contains an @ symbol; inspect carefully.<br>Uses HTTP. HTTPS alone does not prove trust. | PASS |
| 4 | `https://a.b.c.d.e.example.invalid/path` | Many hostname segments | Contains many hostname segments/subdomains. | PASS |
| 5 | `https://xn--example.invalid/` | Punycode-style hostname | Contains a punycode-style hostname. | PASS |

## Notes
- **Text-Only Inspection:** Analyzing URL structure statically is safe and effective as a first line of awareness because the tool never resolves DNS, opens sockets, or contacts potentially harmful servers.
- **HTTPS Misconception:** Many users assume HTTPS guarantees a safe website. In reality, attackers easily obtain free TLS certificates; HTTPS only encrypts transit and does not prove the website's authenticity or trustworthiness.
- **Heuristic Indicators:** Attack techniques like the `@` trick (which hides the true host in credentials), stacked subdomains, punycode spoofing, and raw IP addresses are strong red flags. However, the absence of listed warning signs does not guarantee safety.
