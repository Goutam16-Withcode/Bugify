from agents.code_analysis.subagents.repository_explorer import (
    RepositoryExplorer,
)


def test_repository_explorer(tmp_path):

    # Create repository structure
    src = tmp_path / "src"
    tests = tmp_path / "tests"
    venv = tmp_path / ".venv"

    src.mkdir()
    tests.mkdir()
    venv.mkdir()

    # Source files
    (src / "main.py").write_text(
        'print("hello")'
    )

    (src / "model.py").write_text(
        "class Model:\n    pass"
    )

    # Test file
    (tests / "test_model.py").write_text(
        "def test_model():\n    assert True"
    )

    # Configuration
    (tmp_path / "requirements.txt").write_text(
        "pytest"
    )

    # Should be ignored
    (venv / "ignored.py").write_text(
        "print('ignore me')"
    )

    explorer = RepositoryExplorer()

    result = explorer.explore(str(tmp_path))

    assert result["project_type"] == "python"

    assert "src/main.py" in result["source_files"]
    assert "src/model.py" in result["source_files"]

    assert "tests/test_model.py" in result["test_files"]

    assert "requirements.txt" in result["config_files"]

    assert "src/main.py" in result["entry_points"]

    assert ".venv/ignored.py" not in result["source_files"]