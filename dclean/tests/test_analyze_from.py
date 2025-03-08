from unittest.mock import patch
from dclean.analyze.analyze_from import analyze_from


def test_empty_instruction():
    # Test that analyze_from returns empty string for empty/null inputs
    assert analyze_from({}) == ""
    assert analyze_from(None) == ""
    assert analyze_from({"startline": 0}) == ""


def test_without_value_in_instruction():
    # Test that analyze_from returns empty string when instruction has no 'value' key
    assert analyze_from({"key": "FROM"}) == ""


def test_slim_version():
    # Test that analyze_from returns empty string when image is already using slim version
    assert analyze_from({"value": "ubuntu:slim"}) == ""


def test_alpine_version():
    # Test that analyze_from returns empty string when image is already using alpine version
    assert analyze_from({"value": "alpine:latest"}) == ""


def test_slim_version_with_tag():
    # Test that analyze_from returns empty string when image has a specific tag with slim suffix
    assert analyze_from({"value": "ubuntu:20.04-slim"}) == ""


def test_alpine_version_with_tag():
    # Test that analyze_from returns empty string when image has a specific tag with alpine suffix
    assert analyze_from({"value": "alpine:3.14-slim"}) == ""


def test_slim_version_with_tag_and_digest():
    # Test that analyze_from returns empty string when image has tag, slim suffix, and digest
    assert analyze_from({"value":
                         "ubuntu:20.04-slim@sha256:1234567890abcdef"}) == ""


def test_alpine_version_with_tag_and_digest():
    # Test that analyze_from returns empty string when image has tag, alpine suffix, and digest
    assert analyze_from({"value":
                         "alpine:3.14-slim@sha256:1234567890abcdef"}) == ""


def test_slim_version_with_tag_and_digest_and_registry():
    # Test that analyze_from returns empty string
    # when image has registry, tag, slim suffix, and digest
    assert analyze_from(
        {"value": "docker.io/ubuntu:20.04-slim@sha256:1234567890abcdef"}) == ""


def test_alpine_version_with_tag_and_digest_and_registry():
    # Test that analyze_from returns empty string when image has registry,
    # tag, alpine suffix, and digest
    assert analyze_from(
        {"value": "docker.io/alpine:3.14-slim@sha256:1234567890abcdef"}) == ""


@patch('dclean.analyze.analyze_from.get_repository_tags')
@patch('dclean.analyze.analyze_from.get_recommendation_from')
def test_slim_version_available(mock_get_recommendation, mock_get_tags):
    # Test when slim version is available for the current version
    # Should return recommendation when slim/alpine variants exist for the exact version
    instruction = {"value": "python:3.9", "startline": 0}
    mock_get_tags.side_effect = [
        ["3.9", "3.9-slim", "3.9-alpine"],  # First call with version
        []  # Second call (shouldn't happen in this case)
    ]
    mock_get_recommendation.return_value = "Use slim version"

    result = analyze_from(instruction)

    assert result == "Use slim version"
    mock_get_tags.assert_called_once_with("python", "3.9")
    mock_get_recommendation.assert_called_once_with("python",
                                                    ["3.9-slim", "3.9-alpine"],
                                                    1)


@patch('dclean.analyze.analyze_from.get_repository_tags')
@patch('dclean.analyze.analyze_from.get_recommendation_from')
def test_slim_version_not_for_current_but_available(mock_get_recommendation,
                                                    mock_get_tags):
    # Test when slim version is not available for current version but exists for other versions
    # Should check all tags and return recommendation based on slim variants for other versions
    instruction = {"value": "python:3.9", "startline": 0}
    mock_get_tags.side_effect = [
        ["3.9"],  # First call with version - no slim
        ["3.8", "3.8-slim", "3.9", "3.10-slim"]  # Second call for all tags
    ]
    mock_get_recommendation.return_value = "Use slim version"

    result = analyze_from(instruction)

    assert result == "Use slim version"
    assert mock_get_tags.call_count == 2
    mock_get_recommendation.assert_called_once_with("python",
                                                    ["3.8-slim", "3.10-slim"],
                                                    1)


@patch('dclean.analyze.analyze_from.get_repository_tags')
@patch('dclean.analyze.analyze_from.get_recommendation_from')
def test_no_slim_version_available(mock_get_recommendation, mock_get_tags):
    # Test when no slim version is available at all
    # Should return empty string when no slim/alpine variants exist for any version
    instruction = {"value": "customimage:1.0", "startline": 0}
    mock_get_tags.side_effect = [
        ["1.0"],  # First call with version
        ["0.9", "1.0", "1.1"]  # Second call for all tags
    ]

    result = analyze_from(instruction)

    assert result == ""
    assert mock_get_tags.call_count == 2
    mock_get_recommendation.assert_not_called()
