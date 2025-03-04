from dclean.analyzers.analyze_from import analyze_from


def test_without_instruction():
    assert analyze_from() == []


def test_without_value_in_instruction():
    assert analyze_from({"key": "FROM"}) == []


def test_with_slim_version():
    assert analyze_from({"key": "FROM", "value": "nginx:latest"}) == []
