import re
from urllib.parse import urlparse

# Informational prefixes that do not represent security warning signs
INFO_MESSAGES = (
    "No URL entered",
    "Could not identify",
    "No listed warning",
    "This text is not a valid URL format",
)


def has_warnings(findings):
    """Check if the findings contain actual warning signs rather than info messages."""
    return not findings[0].startswith(INFO_MESSAGES)


def inspect_url(raw_url):
    """Check visible URL text for selected warning signs."""
    url = raw_url.strip()
    findings = []

    if not url:
        return ["No URL entered."]

    candidate = url if "://" in url else "http://" + url

    # Improvement C: Safe parsing to prevent crashes on malformed inputs
    try:
        parsed = urlparse(candidate)
    except ValueError:
        return ["This text is not a valid URL format."]

    host = (parsed.hostname or "").lower()

    if not host:
        return ["Could not identify a hostname."]

    # Check 1: Presence of '@' symbol
    if "@" in candidate:
        findings.append("Contains an @ symbol; inspect carefully.")

    # Check 2: URL length exceeding 100 characters
    if len(url) > 100:
        findings.append("Unusually long URL (over 100 characters).")

    # Check 3: Raw IP address used as hostname
    if re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", host):
        findings.append("Uses an IP address instead of a familiar domain.")

    # Check 4: Excessive hostname segments / subdomains (5 or more parts)
    labels = [part for part in host.split(".") if part]
    if len(labels) >= 5:
        findings.append("Contains many hostname segments/subdomains.")

    # Check 5: Punycode encoded hostname
    if "xn--" in host:
        findings.append("Contains a punycode-style hostname.")

    # Check 6: Unencrypted HTTP connection
    if parsed.scheme.lower() == "http":
        findings.append("Uses HTTP. HTTPS alone does not prove trust.")

    # Fallback if no warnings were triggered
    if not findings:
        findings.append("No listed warning signs found. This does NOT prove safety.")

    return findings


def main():
    print("EWB Phishing URL Awareness Checker")
    print("Text checks only - this program does not open URLs.")

    # Improvement A: Interactive loop allowing multiple checks with exit command
    while True:
        raw_url = input("\nEnter a sample URL (or type q to quit): ")
        if raw_url.strip().lower() in ("q", "quit", "exit"):
            print("Goodbye! Stay alert online.")
            break

        findings = inspect_url(raw_url)

        print("\nResult:")
        for item in findings:
            print("- " + item)

        # Improvement B: Review carefully summary when warnings are detected
        if has_warnings(findings):
            print("\nREVIEW CAREFULLY: " + str(len(findings)) + " warning sign(s) found.")

        print("\nNever enter passwords from unexpected links.")


if __name__ == "__main__":
    main()
