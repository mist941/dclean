from dclean.analyzers.analyze_from import get_repository_version


def test_simple_image():
    """Test simple image name without tag or registry."""
    assert get_repository_version("ubuntu") == "latest"
    assert get_repository_version("nginx") == "latest"


def test_image_with_tag():
    """Test image with tag."""
    assert get_repository_version("ubuntu:20.04") == "20.04"
    assert get_repository_version("nginx:1.21.0") == "1.21.0"


def test_image_with_digest():
    """Test image with digest."""
    assert get_repository_version("ubuntu@sha256:1234567890abcdef") == "latest"


def test_image_with_tag_and_digest():
    """Test image with both tag and digest."""
    assert get_repository_version(
        "ubuntu:20.04@sha256:1234567890abcdef") == "20.04"


def test_image_with_registry():
    """Test image with registry domain."""
    assert get_repository_version("docker.io/ubuntu") == "latest"
    assert get_repository_version("registry.example.com/nginx") == "latest"


def test_image_with_registry_and_tag():
    """Test image with registry domain and tag."""
    assert get_repository_version("docker.io/ubuntu:20.04") == "20.04"


def test_image_with_registry_port():
    """Test image with registry domain and port."""
    assert get_repository_version("localhost:5000/ubuntu") == "latest"
    assert get_repository_version(
        "registry.example.com:5000/nginx") == "latest"


def test_image_with_registry_port_and_tag():
    """Test image with registry domain, port, and tag."""
    assert get_repository_version("localhost:5000/ubuntu:20.04") == "20.04"


def test_image_with_namespace():
    """Test image with namespace."""
    assert get_repository_version("library/ubuntu") == "latest"
    assert get_repository_version("user/app") == "latest"


def test_image_with_registry_and_namespace():
    """Test image with registry domain and namespace."""
    assert get_repository_version("docker.io/library/ubuntu") == "latest"
    assert get_repository_version("registry.example.com/user/app") == "latest"


def test_complex_image_reference():
    """Test complex image reference with registry, namespace, tag, and digest."""
    assert get_repository_version(
        "registry.example.com:5000/user/app:1.0.0@sha256:1234567890abcdef"
    ) == "1.0.0"


def test_complex_version_tags():
    """Test various complex version tag formats."""
    assert get_repository_version("python:3.9-slim") == "3.9-slim"
    assert get_repository_version("node:14-alpine3.12") == "14-alpine3.12"
    assert get_repository_version("ubuntu:focal-20210401") == "focal-20210401"
