import docker
import os
from typing import List

client = docker.from_env()


def analyze_container(dockerfile_path: str) -> List[str]:
    """
    Analyze the container for issues and optimization opportunities.
    """
    build_context = os.path.dirname(dockerfile_path)
    dockerfile = os.path.join(dockerfile_path, "Dockerfile")

    print(f"Building image from {dockerfile_path}")
    try:
        image, logs = client.images.build(
            path=build_context,
            dockerfile=os.path.basename(dockerfile),
            tag="dclean-test")
        for log in logs:
            if isinstance(log, dict) and 'stream' in log:
                print(log['stream'].strip())
            else:
                print(log)
    except Exception as e:
        print(f"Error building image: {e}")
        return [f"Error: {str(e)}"]
