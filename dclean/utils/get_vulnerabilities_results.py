from typing import List, Dict


def get_vulnerabilities_results(vulnerabilities: List[Dict[str, str]]) -> str:
    if not vulnerabilities:
        return "Security scan results: No vulnerabilities found"

    # Count vulnerabilities by severity
    severity_counts = {}
    for vuln in vulnerabilities:
        if vuln.get("type") == "security":
            severity = vuln.get("severity", "Unknown")
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

    # Create summary
    result = "Security Scan Results:\n" + "=" * 50 + "\n\n"

    # Add summary section
    if severity_counts:
        result += "Summary:\n"
        for severity, count in severity_counts.items():
            result += f"    {severity}: {count} issue(s)\n"
        result += "\n"

    # Add detailed findings
    for i, vuln in enumerate(vulnerabilities, 1):
        if vuln.get("type") == "error":
            result += f"Error #{i}:\n"
            result += f"    {vuln.get('message', 'Unknown error')}\n\n"
        elif vuln.get("type") == "security":
            result += f"Vulnerability #{i}:\n"
            result += f"    Severity: {vuln.get('severity', 'Unknown')}\n"
            result += f"    Package: {vuln.get('package', 'Unknown')}\n"
            result += f"    Version: {vuln.get('version', 'Unknown')}\n"

            if vuln.get("fix_version") and vuln.get(
                    "fix_version") != "Unknown":
                result += f"    Fixed in: {vuln.get('fix_version')}\n"

            result += f"    Description: {vuln.get('description', 'No description')}\n\n"

    result += "=" * 50
    return result
