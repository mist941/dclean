from typing import List, Dict
import click


def get_colored_vulnerabilities_results(
        vulnerabilities: List[Dict[str, str]]) -> str:
    if not vulnerabilities:
        return click.style("Security scan results: No vulnerabilities found",
                           fg="green",
                           bold=True)

    # Count vulnerabilities by severity
    severity_counts = {}
    for vuln in vulnerabilities:
        if vuln.get("type") == "security":
            severity = vuln.get("severity", "Unknown")
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

    # Create summary
    result = click.style("Security Scan Results:", fg="yellow",
                         bold=True) + "\n" + "=" * 50 + "\n\n"

    # Add summary section
    if severity_counts:
        result += click.style("Summary:", fg="blue", bold=True) + "\n"
        for severity, count in severity_counts.items():
            severity_color = get_severity_color(severity)
            result += (
                f"    {click.style(severity, fg=severity_color, bold=True)}: {count} issue(s)\n"
            )
        result += "\n"

    # Add detailed findings
    for i, vuln in enumerate(vulnerabilities, 1):
        if vuln.get("type") == "error":
            result += click.style(f"Error #{i}:", fg="red", bold=True) + "\n"
            result += f"    {vuln.get('message', 'Unknown error')}\n\n"
        elif vuln.get("type") == "security":
            severity = vuln.get("severity", "Unknown")
            severity_color = get_severity_color(severity)

            result += click.style(
                f"Vulnerability #{i}:", fg=severity_color, bold=True) + "\n"
            result += click.style("    Severity: ", fg="cyan") + click.style(
                severity, fg=severity_color, bold=True) + "\n"
            result += click.style(
                "    Package: ",
                fg="cyan") + f"{vuln.get('package', 'Unknown')}\n"
            result += click.style(
                "    Version: ",
                fg="cyan") + f"{vuln.get('version', 'Unknown')}\n"

            if vuln.get("fix_version") and vuln.get(
                    "fix_version") != "Unknown":
                result += click.style(
                    "    Fixed in: ", fg="cyan") + click.style(
                        vuln.get("fix_version"), fg="green") + "\n"

            result += click.style(
                "    Description: ",
                fg="cyan") + f"{vuln.get('description', 'No description')}\n\n"

    result += "=" * 50
    return result


def get_severity_color(severity: str) -> str:
    """Return the appropriate color for a given severity level."""
    severity = severity.lower()
    if severity == "critical":
        return "bright_red"
    elif severity == "high":
        return "red"
    elif severity == "medium":
        return "yellow"
    elif severity == "low":
        return "blue"
    else:
        return "white"
