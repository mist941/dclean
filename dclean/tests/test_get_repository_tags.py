from unittest.mock import patch
import pytest
import requests
from dclean.api.get_repository_tags import get_repository_tags


@pytest.fixture
def mock_requests_get():
    with patch("requests.get") as mock_get:
        # Configure the mock with common attributes
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        yield mock_get


@pytest.fixture
def mock_tags_response():
    return {
        "results": [
            {
                "name": "1.21"
            },
            {
                "name": "1.21.1"
            },
            {
                "name": "latest"
            },
        ]
    }


def test_get_repository_tags_without_version_filter(mock_requests_get,
                                                    mock_tags_response):
    repository = "nginx"
    mock_url = (
        f"https://hub.docker.com/v2/repositories/library/{repository}/tags?page=1&page_size=100"
    )
    mock_requests_get.return_value.json.return_value = mock_tags_response
    mock_requests_get.return_value.url = mock_url

    tags = get_repository_tags(repository)
    assert tags == ["1.21", "1.21.1", "latest"]
    mock_requests_get.assert_called_once_with(mock_url)


def test_get_repository_tags_with_version_filter(mock_requests_get,
                                                 mock_tags_response):
    repository = "nginx"
    version = "1.21"
    mock_url = (
        f"https://hub.docker.com/v2/repositories/library/{repository}/tags?page=1&page_size=100"
    )
    mock_requests_get.return_value.json.return_value = mock_tags_response
    mock_requests_get.return_value.url = mock_url

    tags = get_repository_tags(repository, version)
    assert tags == ["1.21", "1.21.1"]
    mock_requests_get.assert_called_once_with(mock_url)


def test_get_repository_tags_invalid_repo(mock_requests_get):
    repository = "invalid_repo"
    mock_requests_get.return_value.json.return_value = {}
    mock_requests_get.return_value.status_code = 404

    tags = get_repository_tags(repository)

    assert tags == []
    assert mock_requests_get.called


def test_get_repository_tags_exception_handling(mock_requests_get):
    repository = "nginx"
    mock_requests_get.side_effect = requests.RequestException("Network error")
    tags = get_repository_tags(repository)

    assert tags == []
    assert mock_requests_get.called


@pytest.mark.parametrize("version_filter,expected_tags", [
    (None, ["1.21", "1.21.1", "latest"]),
    ("1.21", ["1.21", "1.21.1"]),
    ("latest", ["1.21", "1.21.1", "latest"]),
])
def test_get_repository_tags_parametrized(mock_requests_get,
                                          mock_tags_response, version_filter,
                                          expected_tags):
    repository = "nginx"
    mock_requests_get.return_value.json.return_value = mock_tags_response

    tags = get_repository_tags(repository, version_filter)

    assert tags == expected_tags
