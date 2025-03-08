from unittest.mock import patch
import pytest
import requests
from dclean.api.get_repository_tags import get_repository_tags


@pytest.fixture
def mock_requests_get():
    """
    Fixture that mocks the requests.get function.
    
    Returns a mock object configured with common attributes for testing HTTP requests.
    """
    with patch("requests.get") as mock_get:
        # Configure the mock with common attributes
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        yield mock_get


@pytest.fixture
def mock_tags_response():
    """
    Fixture that provides a mock response for Docker Hub tags API.
    
    Returns a dictionary containing sample tag data that mimics the Docker Hub API response.
    """
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
    """
    Test retrieving repository tags without applying any version filter.
    
    Verifies that all tags are returned when no version filter is specified.
    """
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
    """
    Test retrieving repository tags with a version filter applied.
    
    Verifies that only tags matching the specified version filter are returned.
    """
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
    """
    Test behavior when an invalid repository name is provided.
    
    Verifies that an empty list is returned when the repository doesn't exist.
    """
    repository = "invalid_repo"
    mock_requests_get.return_value.json.return_value = {}
    mock_requests_get.return_value.status_code = 404

    tags = get_repository_tags(repository)

    assert tags == []
    assert mock_requests_get.called


def test_get_repository_tags_exception_handling(mock_requests_get):
    """
    Test exception handling when a network error occurs.
    
    Verifies that an empty list is returned when a requests.RequestException is raised.
    """
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
    """
    Parametrized test for retrieving repository tags with different version filters.
    
    Tests multiple scenarios:
    - No version filter (None)
    - Specific version filter ("1.21")
    - "latest" version filter
    
    Verifies that the correct tags are returned for each filter type.
    """
    repository = "nginx"
    mock_requests_get.return_value.json.return_value = mock_tags_response

    tags = get_repository_tags(repository, version_filter)

    assert tags == expected_tags
