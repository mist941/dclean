from dclean.analyze.analyze_from import get_repository_name


def test_simple_image():
    """Test simple image name without tag or registry."""
    assert get_repository_name("ubuntu") == "ubuntu"
    assert get_repository_name("nginx") == "nginx"


def test_image_with_tag():
    """Test image with tag."""
    assert get_repository_name("ubuntu:20.04") == "ubuntu"
    assert get_repository_name("nginx:1.21.0") == "nginx"


def test_image_with_digest():
    """Test image with digest."""
    assert get_repository_name("ubuntu@sha256:1234567890abcdef") == "ubuntu"


def test_image_with_tag_and_digest():
    """Test image with both tag and digest."""
    assert get_repository_name(
        "ubuntu:20.04@sha256:1234567890abcdef") == "ubuntu"


def test_image_with_registry():
    """Test image with registry domain."""
    assert get_repository_name("docker.io/ubuntu") == "ubuntu"
    assert get_repository_name("registry.example.com/nginx") == "nginx"


def test_image_with_registry_and_tag():
    """Test image with registry domain and tag."""
    assert get_repository_name("docker.io/ubuntu:20.04") == "ubuntu"


def test_image_with_registry_port():
    """Test image with registry domain and port."""
    assert get_repository_name("localhost:5000/ubuntu") == "ubuntu"
    assert get_repository_name("registry.example.com:5000/nginx") == "nginx"


def test_image_with_registry_port_and_tag():
    """Test image with registry domain, port, and tag."""
    assert get_repository_name("localhost:5000/ubuntu:20.04") == "ubuntu"


def test_image_with_namespace():
    """Test image with namespace."""
    assert get_repository_name("library/ubuntu") == "library/ubuntu"
    assert get_repository_name("user/app") == "user/app"


def test_image_with_registry_and_namespace():
    """Test image with registry domain and namespace."""
    assert get_repository_name("docker.io/library/ubuntu") == "library/ubuntu"
    assert get_repository_name("registry.example.com/user/app") == "user/app"


def test_complex_image_reference():
    """Test complex image reference with registry, namespace, tag, and digest."""
    assert get_repository_name(
        "registry.example.com:5000/user/app:1.0.0@sha256:1234567890abcdef"
    ) == "user/app"
