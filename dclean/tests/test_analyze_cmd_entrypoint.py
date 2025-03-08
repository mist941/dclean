from dclean.analyze.analyze_cmd_entrypoint import analyze_cmd_entrypoint


def test_analyze_cmd_entrypoint_none_input():
    """Test with None input"""
    result = analyze_cmd_entrypoint(None)
    assert result == ""


def test_analyze_cmd_entrypoint_empty_dict():
    """Test with empty dictionary"""
    result = analyze_cmd_entrypoint({})
    assert result == ""


def test_analyze_cmd_entrypoint_missing_value():
    """Test with dictionary missing 'value' key"""
    result = analyze_cmd_entrypoint({"instruction": "CMD", "startline": 10})
    assert result == ""


def test_analyze_cmd_entrypoint_valid_json_array():
    """Test with valid format"""
    instruction = {
        "instruction": "CMD",
        "value": '["echo", "hello"]',
        "startline": 5
    }
    result = analyze_cmd_entrypoint(instruction)
    assert result == ""


def test_correct_syntax():
    """Test with no valid format"""
    recommendations = analyze_cmd_entrypoint({
        "key": "CMD",
        "value": "[\"npm\", \"start\"]",
        "startline": 0
    })
    assert "Use `[]`" not in recommendations


def test_analyze_cmd_entrypoint_empty_value():
    """Test with empty value."""
    instruction = {"instruction": "CMD", "value": "", "startline": 15}
    result = analyze_cmd_entrypoint(instruction)
    assert result == ""


def test_analyze_cmd_entrypoint_partial_brackets():
    """Test with value that has only opening or closing bracket."""
    instruction = {
        "instruction": "CMD",
        "value": "[echo hello",
        "startline": 20
    }
    result = analyze_cmd_entrypoint(instruction)
    assert result == ""

    instruction = {
        "instruction": "CMD",
        "value": "echo hello]",
        "startline": 25
    }
    result = analyze_cmd_entrypoint(instruction)
    assert result == ""
