from dclean.analyze.analyze_add import analyze_add


def test_empty_instruction():
    """Test with empty instruction."""
    assert analyze_add(None) == ""
    assert analyze_add({}) == ""
    assert analyze_add({"instruction": "ADD"}) == ""


def test_url_detection():
    """Test with URL detection."""
    # Test with various URL formats
    assert "Consider using RUN with" in analyze_add({
        "instruction": "ADD",
        "value": "https://example.com/file.txt",
        "startline": 9
    })
    assert "Consider using RUN with" in analyze_add({
        "instruction": "ADD",
        "value": "http://www.example.com/path/to/file",
        "startline": 9
    })
    assert "Consider using RUN with" in analyze_add({
        "instruction": "ADD",
        "value": "https://domain.co.uk/file.zip",
        "startline": 9
    })
    # Test with multiple sources where one is a URL
    assert "Consider using RUN with" in analyze_add({
        "instruction": "ADD",
        "value": "/local/path https://example.com/file.txt",
        "startline": 9
    })


def test_archive_detection():
    """Test with archive detection."""
    for ext in ['.tar', '.gz', '.zip', '.xz', '.bz2', '.tgz']:
        assert "Consider using COPY instead of ADD when" in analyze_add({
            "instruction":
            "ADD",
            "value":
            f"file{ext}",
            "startline":
            9
        })


def test_no_recommendation_for_valid_add_command():
    """Test with valid ADD command."""
    assert analyze_add({
        "instruction": "ADD",
        "value": "/path/to/regular/file.txt",
        "startline": 9
    }) == ""
    assert analyze_add({
        "instruction": "ADD",
        "value": "/path/to/file1.txt /path/to/file2.txt",
        "startline": 9
    }) == ""


def test_url_takes_precedence_over_archive():
    """Test that URL detection takes precedence over archive detection."""
    assert "Consider using RUN with" in analyze_add({
        "instruction": "ADD",
        "value": "https://example.com/file.txt archive.tar",
        "startline": 9
    })
