from dockerfile_parse import DockerfileParser


def analyze_dockerfile(dockerfilePath: str) -> dict:
    parser = DockerfileParser(path=dockerfilePath)
    print(parser.structure)
