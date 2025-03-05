from dclean.analyzers.analyze_from import analyze_from


def test_without_instruction():
    assert analyze_from() == []


def test_without_value_in_instruction():
    assert analyze_from({"key": "FROM"}) == []
