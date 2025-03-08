import docker
import json
import os
import subprocess
from typing import Dict, List

# Initialize Docker client
try:
    client = docker.from_env()
except Exception as e:
    print(f"Failed to initialize Docker client: {e}")
    client = None


def scan_docker_image(image_name: str) -> Dict:
    """
    Scan a Docker image for vulnerabilities using Trivy.
    
    Args:
        image_name: The name or ID of the Docker image to scan
        
    Returns:
        Dict containing the scan results or error information
    """
    print(f"Scanning image: {image_name}")
    try:
        result = subprocess.run([
            "docker", "run", "--rm", "-v",
            "/var/run/docker.sock:/var/run/docker.sock", "aquasec/trivy",
            "image", "--format", "json", image_name
        ],
                                capture_output=True,
                                text=True,
                                check=True)

        # Parse JSON output
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            print("Failed to parse Trivy output as JSON")
            return {
                "error": "Invalid JSON output",
                "raw_output": result.stdout
            }

    except subprocess.CalledProcessError as e:
        print(f"Trivy scan failed with exit code {e.returncode}")
        return {
            "error": f"Scan failed with exit code {e.returncode}",
            "stderr": e.stderr
        }
    except Exception as e:
        print(f"Error during image scan: {e}")
        return {"error": str(e)}


def analyze_container(dockerfile_path: str) -> List[Dict[str, str]]:
    """
    Analyze the container for security issues and optimization opportunities.
    
    Args:
        dockerfile_path: Path to the directory containing the Dockerfile
        
    Returns:
        List of findings with issue type, severity, and description
    """
    if not client:
        return [{
            "type": "error",
            "message": "Docker client initialization failed"
        }]

    findings = []
    build_context = os.path.dirname(dockerfile_path)
    dockerfile_name = os.path.basename(dockerfile_path)

    if not os.path.exists(dockerfile_path):
        return [{
            "type": "error",
            "message": f"Dockerfile not found at {dockerfile_path}"
        }]

    # Generate a unique tag for the image
    import uuid
    image_tag = f"dclean-test-{uuid.uuid4().hex[:8]}"

    print(f"Building image from {dockerfile_path} with tag {image_tag}")

    try:
        # Build the Docker image
        image, _ = client.images.build(
            path=build_context,
            dockerfile=dockerfile_name,
            tag=image_tag,
            rm=True  # Remove intermediate containers
        )

        # Scan the image for vulnerabilities
        scan_result = scan_docker_image(image.id)

        # Process scan results
        if "error" in scan_result:
            findings.append({
                "type": "error",
                "message": f"Scan error: {scan_result['error']}"
            })
        else:
            # Extract vulnerability information
            if "Results" in scan_result:
                for result in scan_result["Results"]:
                    if "Vulnerabilities" in result:
                        for vuln in result["Vulnerabilities"]:
                            findings.append({
                                "type":
                                "security",
                                "severity":
                                vuln.get("Severity", "Unknown"),
                                "package":
                                vuln.get("PkgName", "Unknown"),
                                "version":
                                vuln.get("InstalledVersion", "Unknown"),
                                "description":
                                vuln.get("Description", "No description"),
                                "fix_version":
                                vuln.get("FixedVersion", "Unknown")
                            })

        # Clean up the image after analysis
        try:
            client.images.remove(image.id, force=True)
            print(f"Removed temporary image {image_tag}")
        except Exception as e:
            print(f"Failed to remove temporary image: {e}")

        return findings

    except docker.errors.BuildError as e:
        print(f"Docker build error: {e}")
        return [{"type": "error", "message": f"Build error: {str(e)}"}]
    except docker.errors.APIError as e:
        print(f"Docker API error: {e}")
        return [{"type": "error", "message": f"Docker API error: {str(e)}"}]
    except Exception as e:
        print(f"Unexpected error: {e}")
        return [{"type": "error", "message": f"Unexpected error: {str(e)}"}]
