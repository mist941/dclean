from dclean.analyze.analyze_run import analyze_run


def test_empty_instruction():
    """Test that empty instructions return an empty recommendations"""
    assert analyze_run([]) == []
    assert analyze_run(None) == []


def test_single_run_instruction():
    """Test that a single run instruction doesn't generate recommendations"""
    instructions = [{
        "instruction": "RUN",
        "value": "apt-get update",
        "startline": 0
    }]
    recommendations = analyze_run(instructions)
    # Should not recommend merging a single command
    assert not any("merge" in rec for rec in recommendations)


def test_apt_install_without_no_recommends():
    """Test recommendation for apt-get install without --no-install-recommends."""
    instructions = [{
        "instruction": "RUN",
        "value": "apt-get install python3",
        "startline": 0
    }]
    recommendations = analyze_run(instructions)
    assert any("--no-install-recommends" in rec for rec in recommendations)


def test_apt_install_with_no_recommends():
    """Test no recommendation when apt-get install uses --no-install-recommends."""
    instructions = [{
        "instruction": "RUN",
        "value": "apt-get install --no-install-recommends python3",
        "startline": 0
    }]
    recommendations = analyze_run(instructions)
    assert not any("--no-install-recommends" in rec for rec in recommendations)


def test_apt_install_without_cache_clean():
    """Test recommendation for apt-get install without cache cleaning."""
    instructions = [{
        "instruction": "RUN",
        "value": "apt-get install python3",
        "startline": 0
    }]
    recommendations = analyze_run(instructions)
    assert any("apt-get clean" in rec for rec in recommendations)


def test_apt_install_with_cache_clean():
    """Test no cache clean recommendation when apt-get clean is used."""
    instructions = [{
        "instruction": "RUN",
        "value": "apt-get install python3 && apt-get clean",
        "startline": 0
    }]
    recommendations = analyze_run(instructions)
    assert not any("apt-get clean" in rec for rec in recommendations)


def test_mergeable_run_commands():
    """Test recommendation to merge consecutive safe RUN commands."""
    instructions = [{
        "instruction": "RUN",
        "value": "apt-get update",
        "startline": 0
    }, {
        "instruction": "RUN",
        "value": "apt-get install python3",
        "startline": 1
    }]
    recommendations = analyze_run(instructions)
    assert any("merge" in rec for rec in recommendations)


def test_unmergeable_run_commands():
    """Test no merge recommendation for commands that are dangerous to merge."""
    instructions = [{
        "instruction": "RUN",
        "value": "apt-get update",
        "startline": 0
    }, {
        "instruction": "RUN",
        "value": "pip install numpy",
        "startline": 1
    }]
    recommendations = analyze_run(instructions)
    assert not any("merge" in rec for rec in recommendations)


def test_separator_between_run_commands():
    """Test no merge recommendation when there's a separator between RUN commands."""
    instructions = [{
        "instruction": "RUN",
        "value": "apt-get update",
        "startline": 0
    }, {
        "instruction": "ENV",
        "value": "PATH=/usr/local/bin:$PATH",
        "startline": 1
    }, {
        "instruction": "RUN",
        "value": "apt-get install python3",
        "startline": 2
    }]
    recommendations = analyze_run(instructions)
    assert not any("merge" in rec for rec in recommendations)


def test_multiple_mergeable_groups():
    """Test multiple groups of mergeable commands."""
    instructions = [{
        "instruction": "RUN",
        "value": "apt-get update",
        "startline": 0
    }, {
        "instruction": "RUN",
        "value": "apt-get install python3",
        "startline": 1
    }, {
        "instruction": "ENV",
        "value": "PATH=/usr/local/bin:$PATH",
        "startline": 2
    }, {
        "instruction": "RUN",
        "value": "apt-get install curl",
        "startline": 3
    }, {
        "instruction": "RUN",
        "value": "apt-get install git",
        "startline": 4
    }]
    recommendations = analyze_run(instructions)

    # Should recommend merging lines 1,2 and 4,5
    merge_recommendations = [rec for rec in recommendations if "merge" in rec]
    assert len(merge_recommendations) == 2
    assert any("Line 1, 2" in rec for rec in merge_recommendations)
    assert any("Line 4, 5" in rec for rec in merge_recommendations)


def test_complex_dockerfile():
    """Test a more complex Dockerfile with various instructions."""
    instructions = [{
        "instruction": "FROM",
        "value": "ubuntu:20.04",
        "startline": 0
    }, {
        "instruction": "RUN",
        "value": "apt-get update",
        "startline": 1
    }, {
        "instruction": "RUN",
        "value": "apt-get install -y python3",
        "startline": 2
    }, {
        "instruction": "WORKDIR",
        "value": "/app",
        "startline": 3
    }, {
        "instruction": "COPY",
        "value": ". /app",
        "startline": 4
    }, {
        "instruction": "RUN",
        "value": "pip install -r requirements.txt",
        "startline": 5
    }, {
        "instruction": "RUN",
        "value": "chmod +x /app/entrypoint.sh",
        "startline": 6
    }, {
        "instruction": "RUN",
        "value": "ln -s /app/bin/app /usr/local/bin/app",
        "startline": 7
    }, {
        "instruction": "CMD",
        "value": "[\"python3\", \"app.py\"]",
        "startline": 8
    }]
    recommendations = analyze_run(instructions)
    # Should recommend merging lines 2,3 and 7,8
    merge_recommendations = [rec for rec in recommendations if "merge" in rec]
    assert len(merge_recommendations) == 2
    assert any("Line 2, 3" in rec for rec in merge_recommendations)
    assert any("Line 7, 8" in rec for rec in merge_recommendations)
    # Should recommend adding --no-install-recommends
    assert any("--no-install-recommends" in rec for rec in recommendations)
    # Should recommend adding cache cleaning
    assert any("apt-get clean" in rec for rec in recommendations)
